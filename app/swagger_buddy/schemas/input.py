from typing import List, Optional

from pydantic import BaseModel, Field

class HeaderInput(BaseModel):
    """Represents an HTTP header parameter in the API endpoint"""
    name: str = Field(
        description="The name of the header (e.g., 'Authorization', 'Content-Type', 'X-API-Key')"
    )
    type: str = Field(
        description="The data type of the header value (e.g., 'string', 'number')"
    )
    descriptive_value: str = Field(
        description="A human-friendly description of what the header should contain, for example if authorization is bearer token, it can be 'Set value to Bearer SECRET_KEY' ,  another example is if content type is json, it can be 'Set value to application/json'"
    )
    required: bool = Field(
        description="Indicates if this header must be included in the request"
    )


class BodyInput(BaseModel):
    """Represents the request body structure for an API endpoint"""
    name: str = Field(
        description="The name of the body parameter or object"
    )
    type: str = Field(
        description="The data type or structure of the field (e.g., 'string', 'number', 'boolean', 'array', 'object')"
    )
    descriptive_value: str = Field(
        description="A detailed explanation of the field, including its purpose, example values, and any constraints"
    )
    required: bool = Field(
        description="Indicates if the request must include this field"
    )


class PathParameterInput(BaseModel):
    """Represents a parameter in the URL path of the endpoint"""
    name: str = Field(
        description="The name of the path parameter as it appears in the URL (e.g., 'userId' in /users/{userId})"
    )
    descriptive_value: str = Field(
        description="A detailed explanation of what the path parameter represents, including format requirements and examples"
    )

class QueryParameterInput(BaseModel):
    """Represents a query parameter in the URL of the endpoint"""
    name: str = Field(
        description="The name of the query parameter as it appears in the URL (e.g., 'page' in ?page=1)"
    )
    descriptive_value: str = Field(
        description="A detailed explanation of the query parameter's purpose, valid values, defaults, and examples"
    )


class CodeInput(BaseModel):
    """Represents a code example in a specific programming language"""
    name: str = Field(
        description="The name of the programming language"
    )
    code: str = Field(
        description="Complete, runnable code example showing how to call the API endpoint, including imports, error handling, and response processing"
    )


class CodeExampleInput(BaseModel):
    """Collection of code examples in different programming languages"""

    curl: CodeInput = Field(
        description="Curl command example"
    )
    python: CodeInput = Field(
        description="Python code example, preferably using modern async/await syntax with popular libraries like requests or httpx"
    )
    javascript:CodeInput = Field(
        description="JavaScript code example, showing both Promise-based and async/await approaches using fetch"
    )
    typescript: CodeInput = Field(
        description="TypeScript code example with proper type definitions, using axios with error handling"
    )
    dart: CodeInput = Field(
        description="Dart code example using dio with proper error handling and model serialization"
    )


class EndpointInput(BaseModel):
    """Represents a single API endpoint with all its details"""
    name: str = Field(
        description="A clear, concise name for the endpoint that describes its purpose (e.g., 'Create User', 'List Transactions')"
    )

    url_of_endpoint: str = Field(
        description="The url of the endpoint, excluding the base url, e.g. /users/123"
    )

    method: str = Field(
        description="The method of the endpoint, e.g. GET, POST, PUT, DELETE"
    )

    description: str = Field(
        description="A comprehensive description of what the endpoint does, including use cases, business rules, and important notes"
    )
    body: Optional[List[BodyInput]] = Field(
        description="The fields that are required or optional to be sent in the request body"
    )
    headers: Optional[List[HeaderInput]] = Field(
        description="List of all headers that can or must be sent with the request"
    )
    path_parameters: Optional[List[PathParameterInput]] = Field(
        description="List of parameters that appear in the endpoint's URL path"
    )
    query_parameters: Optional[List[QueryParameterInput]] = Field(
        description="List of parameters that can be added to the endpoint's URL as query strings"
    )
    code_examples: CodeExampleInput = Field(
        description="Collection of code examples showing how to use the endpoint in different programming languages"
    )


class SectionInput(BaseModel):
    """Represents a logical grouping of related endpoints"""
    name: str = Field(
        description="The name of the section or tag (e.g., 'User Management', 'Payment Operations')"
    )
    description: str = Field(
        description="A detailed overview of this section's purpose and the types of operations it contains"
    )
    endpoints: List[EndpointInput] = Field(
        description="List of all endpoints that belong to this section"
    )


class SwaggerBuddyInput(BaseModel):
    """
    The main schema for transformed Swagger documentation, providing a more
    developer-friendly structure with enhanced descriptions and code examples.
    """
    base_url: Optional[str] = Field(
        description="The base URL for all API endpoints (e.g., 'https://api.example.com/v1')"
    )
    sections: List[SectionInput] = Field(
        description="Organized sections of the API documentation, grouped by functionality or resource type"
    )