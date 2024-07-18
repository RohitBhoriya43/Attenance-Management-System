from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from attendance.serializers import *
from attendance.token import *
from attendance.permission import *
from attendance.utils import *
from attendance.models import *
import threading
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import datetime
from attendance.choices import *
import base64
from django.utils import timezone
from django.db.models import F
import json




