from rest_framework import serializers
from .models import Tasker
from datetime import datetime
from typing import Type, List, Tuple, Dict


RATE_PER_HOUR = 1000


class TaskSerializer(serializers.HyperlinkedModelSerializer):

    """
    Сериалайзер с переопределенным методом обновления записей, для динамического вычисления одного поля (activity).
    Пользователь не может воздействовать на это поле.
    """

    class Meta:
        model: Type[Tasker] = Tasker
        fields: Tuple[str, ...] = ('url', 'id', 'task', 'state', 'activity')
        read_only_fields: List[str] = ['activity']

    def update(self, instance: Tasker, validated_data: Dict[str, str]) -> Tasker:

        instance.task = validated_data.get('task', instance.task)
        instance.state = validated_data.get('state', instance.state)

        if instance.state == 'in-progress':
            start_time = datetime.utcnow()
            time_to_str = start_time.strftime('%Y-%m-%d %H:%M:%S')

            instance.activity = time_to_str

        elif instance.state == 'done':
            time_from_str = datetime.strptime(instance.activity, '%Y-%m-%d %H:%M:%S')
            time_dt = datetime.utcnow() - time_from_str
            result: float = RATE_PER_HOUR / 60 * float(f'{time_dt.seconds}') / 60 % 60

            instance.activity = round(result, 2)

        instance.save()
        return instance
