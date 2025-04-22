import os
import uuid
import aioboto3
import pathlib
import pandas as pd
from io import BytesIO,StringIO
from fastapi import status, UploadFile, File
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import ChatOpenAI, OpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent

from src.database.config import Config
from src.services.users.serializer import QuestionInput
from src.utils.response import (response_structure, ErrorResponseSerializer,
                                SuccessResponseSerializer)

current_path = pathlib.Path().absolute()


class ChatBuilder:

    async def upload_csv_to_s3(self, file: UploadFile = File(...)):
        bucket_name = "llm-jito-demo"
        ext = os.path.splitext(file.filename)[-1] or ".csv"
        unique_filename = f"{uuid.uuid4()}{ext}"
        s3_key = f"uploads/{unique_filename}"

        session = aioboto3.Session(
            aws_access_key_id=Config.ACCESS_KEY,
            aws_secret_access_key=Config.SECRET_KEY
        )

        try:
            # Read the contents of the uploaded file
            file_content = await file.read()

            async with session.client("s3") as s3_client:
                await s3_client.put_object(
                    Bucket=bucket_name,
                    Key=s3_key,
                    Body=file_content,
                    ContentType='text/csv'
                )

        except Exception as e:
            error_message = str(e)
            error_serializer = ErrorResponseSerializer(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Error occurred while uploading CSV to S3",
                data=error_message
            )
            return response_structure(
                serializer=error_serializer,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # Success response
        serializer = SuccessResponseSerializer(
            message="CSV uploaded successfully!",
            data={"bucket": bucket_name, "key": s3_key}
        )
        return response_structure(
            serializer=serializer,
            status_code=status.HTTP_200_OK
        )

    async def read_csv_from_s3(self,bucket_name: str, key: str):
        session = aioboto3.Session(
            aws_access_key_id=Config.ACCESS_KEY,
            aws_secret_access_key=Config.SECRET_KEY
        )

        async with session.client("s3") as s3:
            response = await s3.get_object(Bucket=bucket_name, Key=key)
            content = await response['Body'].read()
            encodings = ['utf-8', 'cp1252', 'ISO-8859-1']
            for enc in encodings:
                try:
                    df = pd.read_csv(BytesIO(content), encoding=enc)
                    break
                except UnicodeDecodeError:
                    continue
            else:
                raise ValueError("Unable to decode CSV with known encodings.")
            return df

    async def open_ai_csv_question(self,request: QuestionInput):
            try:
                bucket_name = "llm-jito-demo"
                key = request.key

                df = await self.read_csv_from_s3(bucket_name,key)
                csv_buffer = StringIO()
                df.to_csv(csv_buffer, index=False)
                csv_buffer.seek(0)

                agent = create_csv_agent(
                    ChatOpenAI(temperature=0, model="gpt-4o-mini"),
                    csv_buffer,
                    verbose=True,
                    agent_type=AgentType.OPENAI_FUNCTIONS,
                    allow_dangerous_code=True
                )
                ans = agent.invoke(request.question)

            except Exception as e:
                # Catch any error that occurs during the processx
                error_message = str(e)
                
                # Serialize the error response
                error_serializer = ErrorResponseSerializer(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="Error occurred while creating conversation",
                    data=error_message
                )
                
                # Return the error response
                return response_structure(
                    serializer=error_serializer,
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            # Sample serializer for success
            serializer = SuccessResponseSerializer(
                message="Question Answer!!!",
                data=ans
            )

            # Successful response example
            return response_structure(
                serializer=serializer,
                status_code=status.HTTP_200_OK
            )