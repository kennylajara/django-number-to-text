from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from num2words.utils import num2english, number_format
from num2words.models.parser import ParseError
from num2words.models.translator import TranslatorError


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def number_to_english(request, *args, **kwargs):
    if request.method == "GET":
        number = request.query_params["number"]
    elif request.method == "POST":
        number = request.data["number"]
    else:
        return Response(
            {"status": "error", "description": "Invalid request method"}, status=400
        )

    if type(number) not in [int, float, str]:
        return Response(
            {"status": "error", "description": "Missing or invalid number"}, status=400
        )
    else:
        try:
            num_in_english = num2english(str(number))
            return Response(
                {
                    "status": "ok",
                    "num_in_english": num_in_english,
                    # NOTE: Uncomment the following lines to enrich the response
                    "formated": number_format(str(number)),
                },
                status=200,
            )
        except (ParseError, TranslatorError) as e:
            return Response({"status": "error", "description": str(e)}, status=400)
