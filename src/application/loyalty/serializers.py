from rest_framework import serializers

from .models import Department, Program, Store


class DepartmentSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='loyalty-api:department-detail')

    class Meta:
        model = Department
        fields = (
            'id', 'url', 'name', 'sys_name',
        )


class ProgramSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='loyalty-api:program-detail')

    class Meta:
        model = Program
        fields = (
            'id', 'url', 'name', 'sys_name',
        )


class StoreSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='loyalty-api:store-detail')
    loyalty_department = DepartmentSerializer()
    loyalty_program = ProgramSerializer()

    class Meta:
        model = Store
        fields = (
            'id', 'url', 'name', 'contact', 'phone', 'address', 'inn', 'agent', 'city', 'price_type', 'loyalty_1c_code',
            'loyalty_1c_user', 'loyalty_plan', 'loyalty_fact', 'loyalty_cashback',  'loyalty_sumcashback',
            'loyalty_debt', 'loyalty_overdue_debt', 'loyalty_department', 'loyalty_program',
        )
