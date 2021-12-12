help_text = {
    'status': '/status - 获取当前状态',
    'add_group': '/add_group <group_id> - 添加群组',
    'remove_group': '/remove_group <group_id> - 移除群组',
    'config_group': '/config_group <group_id> - 配置群组功能',
    'req': '/req <group_id> - 获取某群组原始信息',
    'raw_config': '/raw_config - 检查配置文件'
}

help_text_all = ''

for i in help_text:
    help_text_all = help_text_all + help_text[i] + '\n'


def error_message_generator(func: str):
    return '**Usage**\n' + help_text[func]
