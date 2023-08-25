#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule

# メイン処理
#-----------------------------------------------------------
def main():
    # AnsibleModuleクラス: moduleを作成
    module = AnsibleModule(
      # 引数受け取り
      argument_spec=dict(
        # 引数：target_dict(list型,必須)、検索対象。
        target_dict=dict(type='list', required=True),
        # 引数：target_key(str型,必須)、検索対象キー
        target_key=dict(type='str', required=True),
        # 引数：target_key(str型,必須)、検索文字列
        serach_value=dict(type='str', required=True),
        # 引数：target_strip(str型,def:"")、検索結果出力キー
        serach_key=dict(type='str', required=False, default=None)
      ),
      # 引数チェックを有効
      supports_check_mode=True
    )

    target_dict=module.params['target_dict']
    target_key=module.params['target_key']
    serach_value=module.params['serach_value']
    serach_key=module.params['serach_key']

    discover_value = None
    # 変換対象辞書型リストから1要素ずつ取り出し変換を行う
    for index, t_target_dict in enumerate(target_dict):
      # 換対象キーが存在しなければ、スキップ
      if target_key not in t_target_dict: continue
      if serach_key not in t_target_dict and serach_key != None: continue
      if t_target_dict[target_key] == serach_value:
        if serach_key != None:
          discover_value = t_target_dict[serach_key]
        else:
          discover_value = t_target_dict[target_key]
          
    # 結果dict: resultを作成
    result = dict(
        result=discover_value
    )

    # resultの中身を key=value,の形で出力
    module.exit_json(**result)

if __name__ == '__main__':
    main()
