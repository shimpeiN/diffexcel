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

            # 引数: before(list型, 必須)。差分比較対象辞書型リスト①
            before=dict(type='list', required=True),
            # 引数: after(list型, 必須)。差分比較対象辞書型リスト②
            after=dict(type='list', required=True),
            # 引数: checkkey(str型, 必須)。差分比較リスト突合キー
            checkkey=dict(type='str', required=True),
        ),
        # 引数チェックを有効
        supports_check_mode=True
    )

    before=module.params['before']
    after=module.params['after']
    checkkey=module.params['checkkey']
    
    diff_list=[]
    missing_list=[]
    add_list=[]
    key_name_list=[]
    # 比較対象辞書型リスト①から1要素ずつ取り出し比較を行う
    for t_before in before:
      # 取り出した要素が辞書型でなければ、エラーとする
      if type(t_before) != dict: module.fail_json(msg="before is not list of dict.")
      # 取り出した辞書型にリスト突合キーが存在しなければ、スキップ
      if checkkey not in t_before: continue
      # 突合キーから差分比較対象辞書型リスト①の突合キー値を取得
      key_name=t_before[checkkey]
      #if key_name in key_name_list:
      #  module.fail_json(msg="same key_name exists in before.")
      #else:
      #  key_name_list.append(key_name)
      # 差分比較対象辞書型リスト②から突合キー値と一致する値を取得。存在しなかった場合、Addリストに追加。
      t_after=next((x for x in after if x[checkkey] == key_name), None)
      if t_after == None:
        missing_list.append(key_name)
        continue
      # リスト①から取得した値とリスト②から取得した値が、差分ある場合、キーで一つずつ取り出し、差分比較する
      if t_before != t_after:
        for key  in t_before.keys():
          if key not in t_after:continue
          if type(t_after[key]) == list and type(t_before[key]) != list:t_before[key] = [t_before[key]]
          if type(t_before[key]) == list and type(t_after[key]) != list:t_after[key] = [t_after[key]]
          if t_after[key] != t_before[key]:
            # 差分あるキー値がリストの場合、集合比較し、①のリストと②のリストの両者に存在しない値のみ取得し、diffリストに追加
            if type(t_after[key]) == list:
              t_before_exist=list(set(t_before[key]) - set(t_after[key]))
              t_after_exist=list(set(t_after[key]) - set(t_before[key]))
              if t_before_exist != [] or t_after_exist != []:
                #diff_str=key_name + ":" + key + ":[" + ','.join(t_before_exist) + "]→[" + ','.join(t_after_exist) + ']'
                #diff_list.append(diff_str)
                diff_item={'key_name' : key_name, 'key_col' : key, 'before_exist' : t_before_exist, 'after_exist' : t_after_exist}
                diff_list.append(diff_item)
            else:
              #diff_str=key_name + ":" + key + ":" + str(t_before[key]) + "→" + str(t_after[key])
              #diff_list.append(diff_str)
              diff_item={'key_name' : key_name, 'key_col' : key, 'before_exist' : t_before[key], 'after_exist' : t_after[key]}
              diff_list.append(diff_item)

    # 比較対象辞書型リスト②から1要素ずつ取り出し比較を行う
    key_name_list=[]
    for t_after in after:
      # 取り出した要素が辞書型でなければ、エラーとする
      if type(t_after) != dict: module.fail_json(msg="after is not list of dict.")
      # 取り出した辞書型にリスト突合対象キーが存在しなければ、スキップ
      if checkkey not in t_after: continue
      key_name=t_after[checkkey]
      #if key_name in key_name_list:
      #  module.fail_json(msg="same key_name exists in after.")
      #else:
      #  key_name_list.append(key_name)
      # 差分比較対象辞書型リスト①から突合キー値と一致する値を取得。存在しなかった場合、Missingリストに追加。
      t_before=next((x for x in before if x[checkkey] == key_name), None)
      if t_before == None:
        add_list.append(key_name)
        continue

    # 結果dict: resultを作成
    result = dict(
        chckkey=checkkey,
        Add=add_list,
        Missing=missing_list,
        Change=diff_list
    )

    # resultの中身を key=value,の形で出力
    module.exit_json(**result)

if __name__ == '__main__':
    main()
