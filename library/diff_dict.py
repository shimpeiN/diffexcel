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

            # 引数: before(dict型, 必須)
            before=dict(type='list', required=True),
            # 引数: after(dict型, 必須)
            after=dict(type='list', required=True),
            # 引数: checkkey(str型, 必須)
            checkkey=dict(type='str', required=True),
            # 引数: mode(str型, 必須)
            #mode=dict(type='str', required=True),
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
    for t_before in before:
      key_name=t_before[checkkey]
      t_after=next((x for x in after if x[checkkey] == key_name), None)
      if t_after == None:
        missing_list.append(key_name)
        continue
      if t_before != t_after:
        for key  in t_before.keys():
          if key not in t_after:continue
          if type(t_after) == list and type(t_before) != list:t_before = [t_before]
          if type(t_before) == list and type(t_after) != list:t_after = [t_after]
          if t_after[key] != t_before[key]:
            if type(t_after[key]) == list:
              t_before_exist=list(set(t_before[key]) - set(t_after[key]))
              t_after_exist=list(set(t_after[key]) - set(t_before[key]))
              if t_before_exist != [] or t_after_exist != []:
                diff_str=key_name + ":" + key + ":[" + ','.join(t_before_exist) + "]→[" + ','.join(t_after_exist) + ']'
                diff_list.append(diff_str)   
            else:
              diff_str=key_name + ":" + key + ":" + str(t_before[key]) + "→" + str(t_after[key])
              diff_list.append(diff_str)

    for t_after in after:
      key_name=t_after[checkkey]
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
