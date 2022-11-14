from rest_framework import serializers
from core.models import User
from FORM_MSG.models import Message


class MsgSerializerSIMPLE(serializers.ModelSerializer):
    # author = serializers.StringRelatedField(read_only=True)
    class Meta:
        fields = ('text',)
        model = Message


class UserSerializerSIMPLE(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'username')
        # fields = ('id', 'username', 'messages')
        model = User


class UserSerializer(serializers.ModelSerializer):
    # messages = serializers.StringRelatedField(read_only=True, many=True)  #queryset=...
    messages = MsgSerializerSIMPLE(many=True)

    class Meta:
        # нельзя вместе fields и exclude, и без них по отдельности

        # fields = '__all__'
        fields = ('id', 'username', 'messages')
        # exclude = ('password',)

        model = User


class MsgSerializer(serializers.ModelSerializer):
    # author = serializers.StringRelatedField(read_only=True)
    # author = UserSerializer(read_only=True)  # not many! v1
    author = UserSerializer(read_only=True)  # not many! v2

    # author = serializers.StringRelatedField(source='message.author')  # v3 dw
    # owner = serializers.ReadOnlyField(source='owner.username')

    # or save in perform create

    class Meta:
        fields = ('id', 'name', 'text', 'created_date', 'author', 'msg_length')  # 'author'

        # сериализатор не ждёт в теле POST-запроса поле owner (а если оно придёт, то будет проигнорировано).
        read_only_fields = ('author',)  #('post', 'created', 'OWNER')

        model = Message

    def validate_text(self, value):
        if value == 'not valid':
            raise serializers.ValidationError('Проверьте text (validate_text validator)')
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('post', 'created')
        # model = Comment
