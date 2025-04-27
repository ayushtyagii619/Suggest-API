import os
import openai
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import QueryLog
from .serializers import QueryLogSerializer


openai.api_key = os.getenv("LLM_API_KEY")


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
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that detects tone and intent."},
                    {"role": "user", "content": f"Analyze the tone and intent of: '{query}'. Reply in JSON format: {{'tone':'Tone','intent':'Intent'}}"}
                ],
                temperature=0.3,
                max_tokens=100
            )

            result_text = response['choices'][0]['message']['content']
            result = eval(result_text)  

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

            # Save to Database
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
