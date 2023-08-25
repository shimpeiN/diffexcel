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
        convert_dict=dict(type='dict', required=True),
        # 引数：list_checkkey(str型,必須)、リストチェックキー
        list_checkkey=dict(type='str', required=True),
        # 引数：list_checkkey(str型,必須)、リストチェックキー
        output_file=dict(type='str', required=True),
        # 引数：list_checkkey(str型,必須)、リストチェックキー
        target_file=dict(type='str', required=True)
      ),
      # 引数チェックを有効
      supports_check_mode=True
    )

    target_dict=module.params['target_dict']
    convert_dict=module.params['convert_dict']
    list_checkkey=module.params['list_checkkey']
    output_file=module.params['output_file']
    target_file=module.params['target_file']
    
    output_dict = {}
    output_dict = set_value( target_dict, convert_dict, list_checkkey)
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

def set_value( target_dict, convert_dict, list_checkkey):
  output_dict={}
  for target_key in target_dict:
    if target_key in convert_dict:
      if type(convert_dict[target_key]) == list:
        output_list=[]
        for t_convert in convert_dict[target_key]:
          if type(t_convert) != dict:
            output_dict.setdefault(target_key, convert_dict[target_key])
            break
          else:
            tmp_output={}
            for t_target in target_dict[target_key]:
              if t_convert[list_checkkey] == t_target[list_checkkey]:
                tmp_output = set_value(t_target, t_convert, list_checkkey)
                break
            if tmp_output != {}:
              output_list.append(tmp_output)
            else:
              output_list.append({list_checkkey : t_convert[list_checkkey]})
        if output_list != []:
          output_dict.setdefault(target_key, output_list)
      elif type(convert_dict[target_key]) == dict:
        tmp_output={}
        tmp_output = set_value(target_dict[target_key], convert_dict[target_key])
        output_dict.setdefault(target_key, tmp_output)
      else:
        output_dict.setdefault(target_key,convert_dict[target_key])
  return output_dict

if __name__ == '__main__':
    main()
