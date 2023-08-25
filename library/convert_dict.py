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
        # 引数：target(dict型,必須)、変換対象。辞書型
        target=dict(type='dict', required=True),
        # 引数：target_key(str型,必須)、変換対象値を参照とするためのtargetのキー
        target_key=dict(type='str', required=True),
        # 引数：target_strip(str型,def:"")、変換対象値から除去する文字
        target_strip=dict(type='str', required=False, default=''),
        # 引数：convert_list(list型,必須)、変換参照リスト。targetのtarget_keyの値をconvert_listのbefore_keyの値と突合し、after_keyの値に変換する
        convert_list=dict(type='list', required=True),
        # 引数：before_key(str型,必須)、変換参照リスト内から変換対象値を検索するためのキー
        before_key=dict(type='str', required=True),
        # 引数：after_key(str型,必須)、変換参照リスト内の変換対象値を変換する値のキー
        after_key=dict(type='str', required=True),
        # 引数：skip_list(str型,def:[])、変換対象外とする変換対象値
        skip_list=dict(type='list', required=False, default=[]),
        # 引数：noconvert_failed(bool型,def:False)、変換できなかった場合エラーとするか
        noconvert_failed=dict(type='bool', required=False, default=False),
        add_string=dict(type='str', required=False, default='')
      ),
      # 引数チェックを有効
      supports_check_mode=True
    )

    target=module.params['target']
    target_key=module.params['target_key']
    target_strip=module.params['target_strip']
    convert_list=module.params['convert_list']
    before_key=module.params['before_key']
    after_key=module.params['after_key']
    skip_list=module.params['skip_list']
    noconvert_failed=module.params['noconvert_failed']
    add_string=module.params['add_string']

    
    # 換対象キーが存在しなければ、スキップ
    if target_key in target:
      # 変換値がリストの場合
      if type(target[target_key])==list:
        tmp_list=[]
        for t_target_value in target[target_key]:
          # 変換対象外リストに含まれる場合、変換を行わない
          if t_target_value in skip_list:
            t_value=t_target_value
          # 変換対象外リストに含まれない場合、変換参照リスト内からbefore_keyで検索し、after_keyの値に変換する。
          else:
            # t_value=next((x[after_key] for x in convert_list if x[before_key] == t_target_value.replace(target_strip,"")), None)
            t_value=None
            for x in convert_list:
              # 変換参照リスト内から取り出した値に、before_key,after_keyが含まれない場合、スキップ
              if type(x) != dict: 
                continue 
              if before_key not in x: 
                continue
              if after_key not in x: 
                continue
              if x[before_key] == t_target_value.replace(target_strip,""):
                t_value=add_string + x[after_key]
                break
            # 変換参照リスト内から、変換できなかった場合、noconvert_failedが、Trueならば、エラー。Falseならば、変換を行わない
            if t_value == None:
              if noconvert_failed==False:
                t_value=t_target_value
              else:
                module.fail_json(msg="convart failed. " + target_key + "=" + t_target_value)
          tmp_list.append(t_value)
        target[target_key]=tmp_list
      # 変換対象値がリストでない場合
      else:
        # t_value=next((x[after_key] for x in convert_list if x[before_key] == target[target_key].replace(target_strip,"")), None)
        t_value=None
        for x in convert_list:
          # 変換参照リスト内から取り出した値に、before_key,after_keyが含まれない場合、スキップ
          if type(x) != dict: 
            continue
          if before_key not in x: 
            continue
          if after_key not in x: 
            continue
          if x[before_key] == target[target_key].replace(target_strip,""):
            t_value=add_string + x[after_key]
            break
        if t_value == None:
          if noconvert_failed==False:
            t_value=target[target_key]
          else:
            module.fail_json(msg="convart failed. " + target_key + "=" + target[target_key])
        target[target_key]=t_value
              
    # 結果dict: resultを作成
    result = dict(
        target=target
    )

    # resultの中身を key=value,の形で出力
    module.exit_json(**result)

if __name__ == '__main__':
    main()
