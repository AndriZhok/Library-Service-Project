from rest_framework import serializers
from books.serializers import BookSerializer
from user.serializers import UserSerializer
from borrowing.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    user = UserSerializer(read_only=True)

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
        # Витягуємо книгу
        book = validated_data.get("book")
        # Зменшуємо інвентар
        book.inventory -= 1
        book.save()  # Зберігаємо зміни в базі даних
        return super().create(validated_data)


class BorrowingReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ["actual_return_date"]

    def validate(self, data):
        if self.instance.actual_return_date is not None:
            raise serializers.ValidationError(
                "This borrowing has already been returned."
            )
        return data

    def update(self, instance, validated_data):
        instance.actual_return_date = validated_data.get("actual_return_date")
        # Повертаємо книгу до інвентаря
        instance.book.inventory += 1
        instance.book.save()
        return super().update(instance, validated_data)
