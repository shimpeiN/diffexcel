#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
import yaml
import collections

class FixIndentDumper(yaml.Dumper):
  def increase_indent(self, flow=False, indentless=False):
    return super(FixIndentDumper, self).increase_indent(flow, False)

# メイン処理
#-----------------------------------------------------------
def main():
    # AnsibleModuleクラス: moduleを作成
    module = AnsibleModule(
      # 引数受け取り
      argument_spec=dict(
        # 引数：target(dict型,必須)、検索対象。辞書型
        target_dict=dict(type='dict', required=True),
        # 引数：target_key(str型,必須)、検索対象キー
        compare_dict=dict(type='dict', required=True),
        # 引数：list_checkkey(str型,必須)、リストチェックキー
        list_checkkey=dict(type='str', required=True),
        # output_list(str型,必須)、リストチェックキー
        output_list=dict(type='list', required=True),
        # 引数：list_checkkey(str型,必須)、リストチェックキー
        output_file=dict(type='str', required=True),
        # 引数：list_checkkey(str型,必須)、リストチェックキー
        target_file=dict(type='str', required=True)
      ),
      # 引数チェックを有効
      supports_check_mode=True
    )

    target_dict=module.params['target_dict']
    compare_dict=module.params['compare_dict']
    list_checkkey=module.params['list_checkkey']
    output_list=module.params['output_list']
    output_file=module.params['output_file']
    target_file=module.params['target_file']
    
    output_dict = {}
    output_dict = diff_value( target_dict, compare_dict, list_checkkey, output_list)
    #output_dict = {"config_params": set_dict}
    #yaml = yaml.YAML()
    #yaml.indent(sequence=4, offset=2)
    with open(output_file,"w") as yf:
      yaml.dump(output_dict, yf, default_flow_style=None, allow_unicode=True, Dumper=FixIndentDumper)

    with open(target_file,"w") as yf:
      yaml.dump(target_dict, yf, default_flow_style=None, allow_unicode=True, Dumper=FixIndentDumper)

    # 結果dict: resultを作成
    result = dict(
        result=output_dict
    )

    # resultの中身を key=value,の形で出力
    module.exit_json(**result)

def diff_value( target_dict, compare_dict, list_checkkey, output_list=[]):
  output_dict={}
  add_dict={}
  missing_dict={}
  change_dict={}
  for target_key in target_dict:
    if target_key in compare_dict:
      if list_checkkey == target_key:
        #diff_item={target_key:target_dict[target_key]}
        #output_dict.update(diff_item)
        continue
      if type(target_dict[target_key]) == list:
        #output_list=[]
        discover_list=[]
        for t_target in target_dict[target_key]:
          if type(t_target) != dict:
            target_exist=list(set(target_dict[target_key]) - set(compare_dict[target_key]))
            compare_exist=list(set(compare_dict[target_key]) - set(target_dict[target_key]))
            if target_exist != [] or compare_exist != []:
              diff_item={target_key:{"before":compare_exist,"after":target_exist}}
              change_dict.update(diff_item)
              #change_dict.setdefault(target_key, compare_dict[target_key])
              break
          else:
            tmp_output={}
            for index,t_compare in enumerate(compare_dict[target_key]):
              check_flg=0
              if t_compare[list_checkkey] == t_target[list_checkkey]:
                discover_list.append(index)
                check_flg=1
                tmp_output = diff_value(t_target, t_compare, list_checkkey)
                break
            if tmp_output != {}:
              output_list.append(tmp_output)
            elif tmp_output == {} and check_flg == 0:
              tmp_add_dict={}
              #for item in t_target:
              #  if item in output_list:
              #    tmp_dict.update({item:{"add":t_target[item]}})
              if list_checkkey in t_target:
                tmp_add_dict.update({list_checkkey:t_target[list_checkkey]})
              if tmp_dict!={}:
                if list_checkkey in t_target:
                  tmp_dict.update({list_checkkey:t_target[list_checkkey]})
                output_list.append(tmp_dict)
        for index, t_compare in enumerate(compare_dict[target_key]):
          if index not in discover_list:
            tmp_dict={}
            for item in t_compare:
              if item in output_list:
                tmp_dict.update({item:{"missing":t_compare[item]}})
            if tmp_dict!={}:
              if list_checkkey in t_compare:
                tmp_dict.update({list_checkkey:t_compare[list_checkkey]})
              output_list.append(tmp_dict)
        if output_list != []:
          output_dict.update({target_key:output_list})
      elif type(target_dict[target_key]) == dict:
        tmp_output={}
        tmp_output = diff_value(target_dict[target_key], compare_dict[target_key], list_checkkey)
        if tmp_output != {}:
          output_dict.update({target_key:tmp_output})
      else:
        if target_dict[target_key] != compare_dict[target_key]:
          diff_item={target_key:{"before":compare_dict[target_key],"after":target_dict[target_key]}}
          change_dict.update(diff_item)
    else:
      diff_item={target_key:target_dict[target_key]}
      add_dict.update(diff_item)
  if output_dict != {}:
    if list_checkkey in target_dict:
      output_dict.update({list_checkkey:target_dict[list_checkkey]})
  return output_dict

if __name__ == '__main__':
    main()
