from application.agent.models import Store as AgentStore

from .models import Store, Department, Program


def loyalty_1c_stores(data):

    for store in data['GO']:

        # Save temp store
        try:
            obj = Store.objects.get(loyalty_1c_code=store['id'])
        except Store.DoesNotExist:
            obj = Store()

        obj.loyalty_1c_code = store['id']
        obj.loyalty_1c_user = store['id_user']
        obj.name = store['name']
        obj.contact = store['contact']
        obj.phone = store['telephone'][:30]
        obj.inn = store['INN'][:12]
        obj.city = store['region']
        obj.address = store['adress']
        obj.agent = store['agent']

        # obj.loyalty_plan = store['plan']
        # obj.loyalty_fact = store['fact']
        # obj.loyalty_cashback = store['cashback']
        # obj.loyalty_sumcashback = store['sumcashback']
        obj.loyalty_debt = store['debt']
        obj.loyalty_overdue_debt = store['overdue_debt']
        obj.price_type = store['PriceType']

        try:
            department = Department.objects.get(sys_name=store['channel'])
        except Department.DoesNotExist:
            department = Department(sys_name=store['channel'], name=store['channel'])
            department.save()
        obj.loyalty_department = department

        try:
            program = Program.objects.get(sys_name=store['program'])
        except Program.DoesNotExist:
            program = Program(sys_name=store['program'], name=store['program'])
            program.save()
        obj.loyalty_program = program

        obj.save()

        # Update Store
        try:
            items = AgentStore.objects.filter(loyalty_1c_code=store['id'])
            for obj in items:
                # obj.loyalty_plan = store['plan']
                # obj.loyalty_fact = store['fact']
                # obj.loyalty_cashback = store['cashback']
                # obj.loyalty_sumcashback = store['sumcashback']
                obj.loyalty_debt = store['debt']
                obj.loyalty_overdue_debt = store['overdue_debt']
                obj.agent = store['agent']
                obj.price_type = store['PriceType']
                obj.save()

        except AgentStore.DoesNotExist:
            pass

    return 'Ok'
