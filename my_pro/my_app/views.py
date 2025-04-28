
import os
import google.generativeai as genai
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import QueryLog
from .serializers import QueryLogSerializer
import re
import json

# Load Gemini API Key from .env
genai.configure(api_key=os.getenv("LLM_API_KEY"))


ACTIONS = {
    "ORDER_FOOD": "Order Food Online",
    "FIND_RECIPE": "Find Food Recipes",
    "ASK_HELP": "Ask for Help",
    "SHARE_NEWS": "Share Some News",
}

class Suggest_View(APIView):

    def post(self, request):
        query = request.data.get('query')
        if not query:
            return Response({"error": "Query is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

            response = model.generate_content(
                f"Analyze the following message for tone and intent: '{query}'. "
                f"Reply in JSON format like this: {{'tone':'Tone','intent':'Intent'}}"
            )

            result_text = response.text.strip()
            match = re.search(r"\{.*\}", result_text, re.DOTALL)
            if match:
                json_text = match.group(0)
                result = json.loads(json_text.replace("'", '"'))  
            else:
                return Response({"error": "Invalid response format from Gemini"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            tone = result.get('tone')
            intent = result.get('intent')

            
            suggestions = []
            if intent:
                if "order" in intent.lower():
                    suggestions.append({"action_code": "ORDER_FOOD", "display_text": ACTIONS["ORDER_FOOD"]})
                if "recipe" in intent.lower():
                    suggestions.append({"action_code": "FIND_RECIPE", "display_text": ACTIONS["FIND_RECIPE"]})
                if "help" in intent.lower():
                    suggestions.append({"action_code": "ASK_HELP", "display_text": ACTIONS["ASK_HELP"]})
                if "news" in intent.lower():
                    suggestions.append({"action_code": "SHARE_NEWS", "display_text": ACTIONS["SHARE_NEWS"]})

            
            query_log = QueryLog.objects.create(
                query=query,
                tone=tone,
                intent=intent,
                suggested_actions=suggestions
            )

            serializer = QueryLogSerializer(query_log)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
