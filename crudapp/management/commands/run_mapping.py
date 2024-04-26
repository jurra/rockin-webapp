from mappings import *

base_path = './_no_data'

df = pd.read_csv(base_path + '/raw/cores/tb_core.csv', encoding='utf-8')
column_names_list = df.columns.tolist()

column_mappings, data_mappings, ignore_columns = load_mappings(base_path + '/raw/cores/mapping.yaml')
apply_mappings(csv_file=base_path + '/raw/cores/tb_core.csv', column_mappings=column_mappings,  data_mappings=data_mappings, column_to_modify=None, output_file=base_path + '/processed/tb_core.csv', ignore_columns=ignore_columns)

df = pd.read_csv(base_path + '/processed/tb_core.csv', encoding='utf-8')
print(df.columns.tolist())

# from crudapp.management.commands import *
# from crudapp.management.commands.mappings import *
# users = load_mappings("./_no_data/raw/users/mappings.yaml")
# users
# ({'id': 'id', 'user_name': 'username'}, {}, ['last_login', 'is_superuser', 'password'])
# column_mappings, data_mappings, ignore_columns = users
# column_mappings
# {'id': 'id', 'user_name': 'username'}
# processed = apply_mappings("_no_data/raw/users/tb_users.csv", column_mappings, data_mappings, 'id', "_no_data/processed/tb_users.csv", ignore_columns)
