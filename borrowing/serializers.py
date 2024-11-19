from rest_framework import serializers

from books.serializers import BookSerializer
from borrowing.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "user",
            "book",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
        ]


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ["id", "user", "book", "borrow_date", "expected_return_date"]

    def validate(self, data):
        if data["book"].inventory <= 0:
            raise serializers.ValidationError("The book is out of stock.")
        return data

    def create(self, validated_data):
        book = validated_data["book"]
        book.inventory -= 1
        book.save()
        return super().create(validated_data)


class BorrowingReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ["actual_return_date"]

    def update(self, instance, validated_data):
        if not instance.actual_return_date:
            instance.book.inventory += 1
            instance.book.save()
        return super().update(instance, validated_data)
