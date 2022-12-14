from rest_framework import serializers
from core.models import User
from FORM_MSG.models import Message


class MsgSerializerSIMPLE(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'text', 'created_date')
        model = Message


class UserSerializerSIMPLE(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'username')
        model = User


class UserSerializer(serializers.ModelSerializer):
    messages = MsgSerializerSIMPLE(many=True)

    class Meta:
        fields = ('id', 'username', 'messages')

        model = User


class MsgSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        fields = ('id', 'name', 'text', 'created_date', 'author', 'msg_length')
        read_only_fields = ('author',)

        model = Message

    def validate_text(self, value):
        if value == 'not valid':
            raise serializers.ValidationError('Проверьте text (validate_text validator)')
        return value

