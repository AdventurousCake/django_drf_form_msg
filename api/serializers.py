from rest_framework import serializers

from FORM_MSG.models import Message, Like, Comment
from core.models import User


class LikeSerializerSIMPLE2(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    message_text = serializers.ReadOnlyField(source='message.text')

    class Meta:
        fields = ('id', 'username', 'message_text', 'created_date')
        model = Like


class LikeSerializerSIMPLE(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'user', 'message', 'created_date')
        model = Like


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


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    message_id = serializers.ReadOnlyField(source='message.id')
    message_text = serializers.ReadOnlyField(source='message.text')
    comment_text = serializers.ReadOnlyField(source='text')

    class Meta:
        fields = ('id', 'user', 'message_id', 'comment_text', 'message_text', 'created_date')
        # read_only_fields = ('post', 'created')
        model = Comment
