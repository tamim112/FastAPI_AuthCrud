from fastapi import FastAPI, HTTPException, status ,APIRouter,Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy import Boolean, Column, Integer, String, text
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Annotated
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt, JWTError
from starlette import status