
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
    "FIND_NEARBY_PIZZERIA": "Find nearby pizza restaurants",
    "PLACE_ONLINE_ORDER": "Place an online pizza order",
    "BROWSE_PIZZA_MENU": "Browse pizza menus",
    "ASK_FOR_HELP": "Ask for help",
    "SHARE_FOOD_NEWS": "Share latest food news",
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
                    suggestions.append({"action_code": "PLACE_ONLINE_ORDER", "display_text": "Place an online pizza order"})
                    suggestions.append({"action_code": "FIND_NEARBY_PIZZERIA", "display_text": "Find nearby pizza restaurants"})
                    suggestions.append({"action_code": "BROWSE_PIZZA_MENU", "display_text": "Browse pizza menus"})
                elif "help" in intent.lower():
                    suggestions.append({"action_code": "ASK_FOR_HELP", "display_text": "Ask for help"})
                elif "news" in intent.lower():
                    suggestions.append({"action_code": "SHARE_FOOD_NEWS", "display_text": "Share latest food news"})

            
            query_log = QueryLog.objects.create(
                query=query,
                tone=tone,
                intent=intent,
                suggested_actions=suggestions
            )
            final_response = {
                "query": query,
                "analysis": {
                    "tone": tone,
                    "intent": intent
                },
                "suggested_actions": suggestions
            }

            

            return Response(final_response, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
