import json
import yaml
import httpx
from uuid import UUID
from pydantic import HttpUrl
from  fastapi  import UploadFile
from sqlmodel import select, desc
from settings.config import settings
from sqlalchemy.orm import joinedload
from langchain_openai import ChatOpenAI
from .schemas.create_project import CreateProjectSchema
from ..database.config import DatabaseSession
from langchain_core.prompts import ChatPromptTemplate
from app.swagger_buddy.schemas.input import SwaggerBuddyInput
from app.common.exceptions import BadRequestException, NotFoundException
from .models import Project, Section, Endpoint, CodeExample, Body, Header, PathParameter, QueryParameter

class ProjectService:
    def __init__(self, session: DatabaseSession):
        self.session = session


    async def create_project(self, parse_swagger_format_input: CreateProjectSchema):
        if not parse_swagger_format_input.swagger_url and not parse_swagger_format_input.swagger_file:
            raise BadRequestException(message="Either swagger_url or swagger_file must be provided")

        if parse_swagger_format_input.swagger_url:
            swagger_data = await self._fetch_and_parse_swagger_from_url(parse_swagger_format_input.swagger_url)
        else:
            swagger_data = await self._parse_swagger_from_file(parse_swagger_format_input.swagger_file)

        import pprint
        pprint.pprint(swagger_data)

        # client = ChatOpenAI(api_key=settings.OPENAI_API_KEY, model_name="gpt-4o-2024-08-06")
        client = ChatOpenAI(api_key=settings.OPENAI_API_KEY, model_name="gpt-4.1", temperature=0.1)


        prompt = ChatPromptTemplate.from_messages([
                ("system", 
                    """You are an expert API documentation specialist tasked with transforming Swagger/OpenAPI documentation into developer-friendly, comprehensive documentation.

                    Your goal is to:
                    1. Analyze the provided Swagger documentation thoroughly
                    2. Extract all endpoints, parameters, and data structures
                    3. Generate clear, detailed descriptions for each component
                    4. Create practical code examples in multiple programming languages
                    5. Organize the information in a logical, hierarchical structure
                    6. Ensure all responses follow the exact schema structure provided

                    For each endpoint's request and response bodies:
                    - List every field with its exact type and format
                    - Clearly mark which fields are required vs optional
                    - Provide example values that make sense in the business context
                    - Explain any validation rules or constraints
                    - Document relationships between components and schemas
                    - Include descriptions of nested objects and their structures
                    - Note any enum values or specific format requirements
                    - Explain any default values and their significance

                    Focus on making the documentation practical and easy to understand for frontend developers.
                    Your output must strictly conform to the SwaggerBuddyInput schema structure."""
                ),
                ("human", 
                    """Please transform the following Swagger documentation into a comprehensive, developer-friendly format:
                    Base URL: {base_url}
                    Swagger Data: {swagger_data}

                    If the input is large, focus on the most commonly used endpoints and provide a good representative sample.
                    Ensure proper error handling and include authentication details where available."""
                )
            ])

        chain = prompt | client.with_structured_output(SwaggerBuddyInput)

        # prompt = ChatPromptTemplate.from_messages([
        #     ("system", 
        #         """You are an expert API documentation specialist and data extraction expert. tasked with transforming Swagger/OpenAPI documentation into developer-friendly, comprehensive documentation. Your goal is to:

        #         1. Analyze the provided Swagger documentation thoroughly
        #         2. Extract all endpoints, parameters, and data structures
        #         3. Generate clear, detailed descriptions for each component
        #         4. Create practical code examples in multiple programming languages
        #         5. Organize the information in a logical, hierarchical structure
        #         6. Ensure all responses follow the exact schema structure provided

        #         For each endpoint's request and response bodies:
        #         - List every field with its exact type and format
        #         - Clearly mark which fields are required vs optional
        #         - Provide example values that make sense in the business context
        #         - Explain any validation rules or constraints
        #         - Document relationships between components and schemas
        #         - Include descriptions of nested objects and their structures
        #         - Note any enum values or specific format requirements
        #         - Explain any default values and their significance

        #         For authentication and security:
        #         - Detail all security schemes (API keys, OAuth, etc.)
        #         - Explain where security credentials should be placed (headers, body, etc.)
        #         - Provide examples of properly formatted authentication
        #         - Note any token formats or requirements

        #         For error handling:
        #         - Document all possible error responses
        #         - Explain what triggers each error
        #         - Provide the complete error response structure
        #         - Include examples of common error scenarios

        #         Focus on making the documentation practical and easy to understand for frontend developers. Include:
        #         - Clear explanations of authentication requirements
        #         - Detailed parameter descriptions with examples
        #         - Common use cases and scenarios
        #         - Best practices for error handling
        #         - Real-world code examples that demonstrate proper implementation

        #         Your output must strictly conform to the SwaggerBuddyInput schema structure, with all required fields and proper formatting."""
        #     ),

        #     ("human", 
        #         """Please transform the following Swagger documentation into a comprehensive, developer-friendly format:
        #         The base url is: {base_url}
        #         The swagger data is: {swagger_data}

        #         Requirements:
        #         1. Group related endpoints into logical sections
        #         2. Provide detailed descriptions that explain the business purpose of each endpoint
        #         3. Include code examples in Python, JavaScript, TypeScript, and Flutter
        #         4. Ensure all examples are complete and runnable, including:
        #            - Required imports
        #            - Error handling
        #            - Response processing
        #            - Authentication setup
        #         5. Add helpful comments in code examples to explain key steps
        #         6. For each request/response body:
        #            - List ALL fields from the schema definitions
        #            - Clearly indicate required vs optional fields
        #            - Show the exact data type and format for each field
        #            - Provide realistic example values
        #            - Explain any field constraints or validations
        #            - Document nested object structures
        #            - Include enum values where applicable
        #         7. For error responses:
        #            - Document the complete error structure
        #            - Show example error responses
        #            - Explain what triggers each error
        #            - Include error handling code examples
        #         8. Explain any rate limits, pagination, or special considerations
        #         9. Include authentication details:
        #            - Security scheme types
        #            - Header or parameter names
        #            - Token formats
        #            - Example authentication code

        #         Format your response exactly according to the schema, maintaining all required fields and proper data types. Make sure to resolve and document all schema references ($ref) to their complete definitions."""
        #     )
        # ])

        # chain = prompt | client.with_structured_output(SwaggerBuddyInput)

        result: SwaggerBuddyInput = chain.invoke({"swagger_data": swagger_data, "base_url": parse_swagger_format_input.base_url})

        project = Project(
            name=parse_swagger_format_input.project_name, 
            base_url=str(parse_swagger_format_input.base_url), 
            sections=[
                Section(name=section.name, description=section.description, endpoints=[
                    Endpoint(
                        name=endpoint.name, 
                        url_of_endpoint=endpoint.url_of_endpoint, 
                        description=endpoint.description, 
                        method=endpoint.method,
                        body=[Body(name=body.name, type=body.type, descriptive_value=body.descriptive_value, required=body.required) for body in endpoint.body or []],
                        headers=[Header(name=header.name, type=header.type, descriptive_value=header.descriptive_value, required=header.required) for header in endpoint.headers or []],
                        path_parameters=[PathParameter(name=path_parameter.name, descriptive_value=path_parameter.descriptive_value) for path_parameter in endpoint.path_parameters or []],
                        query_parameters=[QueryParameter(name=query_parameter.name, descriptive_value=query_parameter.descriptive_value) for query_parameter in endpoint.query_parameters or []],
                        code_examples=[
                            CodeExample(
                                language=value['name'], 
                                language_code=key, 
                                code=value['code']
                            ) for key, value in endpoint.code_examples.model_dump().items()
                    ]) for endpoint in section.endpoints
                ]) for section in result.sections
            ]
        )

        new_project = await self.session.save(project)

        return new_project
    

    async def get_projects(self):
        statement = select(Project).options(
            joinedload(Project.sections)
            .joinedload(Section.endpoints)
        ).order_by(desc(Project.created_at))
        
        result = await self.session.exec(statement)
        projects = result.unique().all()

        return projects


    async def get_project(self, project_id: UUID):

        results = await self.session.exec(
            select(Project)
            .where(Project.id == project_id)
            .options(
                joinedload(Project.sections)
                .joinedload(Section.endpoints)
                .joinedload(Endpoint.code_examples)
            )
            .options(
                joinedload(Project.sections)
                .joinedload(Section.endpoints)
                .joinedload(Endpoint.body)
            )
            .options(
                joinedload(Project.sections)
                .joinedload(Section.endpoints)
                .joinedload(Endpoint.headers)
            )
            .options(
                joinedload(Project.sections)
                .joinedload(Section.endpoints)
                .joinedload(Endpoint.path_parameters)
            )
            .options(
                joinedload(Project.sections)
                .joinedload(Section.endpoints)
                .joinedload(Endpoint.query_parameters)
            )
        )

        project: Project = results.unique().first()

        return project

    async def delete_project(self, project_id: UUID):

        project = await self.session.find_by_id(Project, project_id)

        if not project:
            raise NotFoundException("Project not found")

        await self.session.delete(project)
    

    async def _fetch_and_parse_swagger_from_url(self, url: HttpUrl) -> dict:
        async with httpx.AsyncClient() as session:
            try:
                response = await session.get(
                    url=str(url),
                    timeout=10,
                    auth=("admin", "password")
                )
                response.raise_for_status()

                content_type = response.headers.get("Content-Type", "")
                if "application/json" in content_type:
                    return dict(response.json())

                try:
                    return yaml.safe_load(response.text)
                except Exception as e:
                    raise BadRequestException(message=f"Failed to parse Swagger YAML: {str(e)}")

            except httpx.HTTPStatusError as e:
                try:
                    error_detail = e.response.json().get("message", str(e))
                except Exception:
                    error_detail = f"HTTP {e.response.status_code}: {str(e)}"
                raise BadRequestException(message=error_detail)

            except httpx.RequestError as e:
                print(e)
                raise BadRequestException(message=f"Failed to fetch Swagger: {str(e)}")

            except json.JSONDecodeError:
                raise BadRequestException(message="Invalid Swagger format: Response is not valid JSON")

            except Exception as error:
                print(f"Unexpected error: {error}")
                raise BadRequestException(message="An unexpected error occurred while fetching the Swagger file")
            

    async def _parse_swagger_from_file(self, file: UploadFile) -> dict:
        content_type = file.content_type

        if content_type in ["application/json", "application/x-json", "text/json", "text/x-json"]:
            return dict(json.loads(file.file.read()))
        elif content_type in ["application/yaml", "application/x-yaml", "text/yaml", "text/x-yaml"]:
            return dict(yaml.safe_load(file.file.read()))
        else:
            raise BadRequestException(message="Unsupported file type, only JSON and YAML are supported")

