from adrf import generics
from rest_framework import status, serializers
from rest_framework.response import Response
from adrf.views import APIView
from adrf.mixins import UpdateModelMixin
from adrf.serializers import Serializer, ModelSerializer
from .models import Vocab
from .clients import get_pronounce, get_masked_definition_and_examples
from users.permissions import AsyncIsOTPVerified

class WordSerializer(ModelSerializer):
    class Meta:
        model = Vocab
        fields = '__all__' 


class WordsAPIView(generics.ListCreateAPIView):

    permission_classes = [AsyncIsOTPVerified]

    queryset = Vocab.objects.all()
    serializer_class = WordSerializer


class WordAPIView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [AsyncIsOTPVerified]

    queryset = Vocab.objects.all()
    serializer_class = WordSerializer
    lookup_url_kwarg = 'id' 

class SpellingGetSerializer(Serializer):
    audio_link = serializers.CharField()
    word_id = serializers.IntegerField()

class SpellingPostSerializer(Serializer):
    word = serializers.CharField()
    word_id = serializers.IntegerField()

class SpellingAPIView(APIView): 
    permission_classes = [AsyncIsOTPVerified]
    
    async def get(self, request):
        random_word = await Vocab.objects.order_by('?').filter(is_spelling=True, last_successive_successes__lt=10).afirst()
        
        if not random_word.audio_url:
            audio_url = await get_pronounce(random_word.word, random_word.id)
            random_word.audio_url = audio_url
            await random_word.asave()
        else:
            audio_url = random_word.audio_url

        serializer = SpellingGetSerializer(data={
            "word_id": random_word.id,
            "audio_link": audio_url 
        })
        
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    async def post(self, request):
        serializer = SpellingPostSerializer(data=request.data)
        if serializer.is_valid():
            written_word = serializer.validated_data['word']
            word_id = serializer.validated_data['word_id']

            try:
                correct_word = await Vocab.objects.aget(id=word_id)
            except Vocab.DoesNotExist:
                return Response({"error": "Word not found"}, status=status.HTTP_404_NOT_FOUND)

            is_correct = written_word.lower() == correct_word.word.lower()

            if is_correct:
                correct_word.last_successive_successes += 1
                correct_word.total_success += 1
            else:
                correct_word.last_successive_successes += 0
                correct_word.total_fails += 1

            await correct_word.asave()

            return Response({
                "is_correct": is_correct,
                "correct_word": correct_word.word,
                "submit_word": serializer.validated_data['word'],
            })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class PracticeGetSerializer(Serializer):
    prompt = serializers.CharField()
    word_id = serializers.IntegerField()

class PracticePostSerializer(Serializer):
    word = serializers.CharField()
    word_id = serializers.IntegerField()

class PracticeAPIView(APIView): 
    permission_classes = [AsyncIsOTPVerified]
    
    async def get(self, request):
        random_word = await Vocab.objects.order_by('?').filter(is_spelling=False, last_successive_successes__lt=10).afirst()

        prompt = await get_masked_definition_and_examples(random_word.word)

        serializer = PracticeGetSerializer(data={
            "word_id": random_word.id,
            "prompt": prompt
        })
        
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    async def post(self, request):
        serializer = PracticePostSerializer(data=request.data)
        if serializer.is_valid():
            written_word = serializer.validated_data['word']
            word_id = serializer.validated_data['word_id']

            try:
                correct_word = await Vocab.objects.aget(id=word_id)
            except Vocab.DoesNotExist:
                return Response({"error": "Word not found"}, status=status.HTTP_404_NOT_FOUND)

            is_correct = written_word.lower() == correct_word.word.lower()

            if is_correct:
                correct_word.last_successive_successes += 1
                correct_word.total_success += 1
            else:
                correct_word.last_successive_successes += 0
                correct_word.total_fails += 1

            await correct_word.asave()

            return Response({
                "is_correct": is_correct,
                "correct_word": correct_word.word,
                "submit_word": serializer.validated_data['word'],
            })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




