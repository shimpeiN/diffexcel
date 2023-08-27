#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
import yaml
import requests
from ansible.module_utils.urls import open_url
import json

# メイン処理
#-----------------------------------------------------------
def main():
    # AnsibleModuleクラス: moduleを作成
    module = AnsibleModule(

        # 引数受け取り
        argument_spec=dict(
            # nsxtユーザ
            user=dict(type='str', required=True),
            # nsxtパスワード
            password=dict(type='str', required=True),
            validate_certs=dict(type='bool', required=True),
            # nsxt reset api url
            api_policy=dict(type='str', required=True),
            # 引数: after(list型, 必須)。差分比較対象ファイルリスト
            target_file_list=dict(type='list', required=True),
            # 引数: target_file_strip(str型, 必須)。出力時に、差分比較対象ファイルパスから除去する文字列
            target_file_strip=dict(type='str', required=True),
            # 引数: checkkey(str型, 必須)。差分比較する際の突合キー
            checkkey=dict(type='str', required=True),
            # 引数: GW type(str型, 必須)。gw type
            gw_type=dict(type='str', required=True, choices=['gfw', 'dfw'])
        ),
        # 引数チェックを有効
        supports_check_mode=True
    )

    checkkey=module.params['checkkey']
    target_file_list=module.params['target_file_list']
    user=module.params['user']
    password=module.params['password']
    validate_certs=module.params['validate_certs']
    api_policy=module.params['api_policy']
    target_file_strip=module.params['target_file_strip']
    
    diff_list=[]
    missing_list=[]
    add_list=[]
    missing_key_list=[]
    if gw_type == 'gfw':
      gw_policy == 'gateway-policies'
    elif  gw_type == 'dfw':
      gw_policy = 'security-policies'
    
    # fwセクション一覧を取得
    url= api_policy + '/infra/domains/default/' + gw_policy
    policy_list=get_api_request(module, url, validate_certs, user, password)

    # サービス一覧を取得
    url= api_policy + '/infra/services'
    service_list=get_api_request(module, url, validate_certs, user, password)
    
    strip_len=len(target_file_strip)
    # 差分比較対象ファイルリストから、1ファイルごと、読み込む
    for target_file in target_file_list:
      with open(target_file['path'], 'r') as yml:
        params = yaml.safe_load(yml)
        
        #セクション一覧から比較対象のセクションが存在するか
        discover_value = None
        #　比較対象セクションが、policy_list(実機設定)に存在するかチェック
        for index, t_target_dict in enumerate(policy_list['results']):
          if checkkey not in t_target_dict: continue
          if t_target_dict[checkkey] == params['config_params'][checkkey]:
            discover_value = t_target_dict[checkkey]
        
        # 実機設定に比較対象のセクションが存在する場合、差分比較を行う
        if discover_value != None:
          # 比較対象ルールのサービスを変換処理
          target_rules=convert_listofdict(module, params['config_params']['rules'], "services", "/infra/services/", service_list['results'], checkkey, "path", ['ANY'], False)
          # 実機ルール一覧取得
          url= api_policy + '/infra/domains/default/' + gw_policy + '/' + params['config_params'][checkkey]
          fw_rules=get_api_request(module, url, validate_certs, user, password)
          
          #before=fw_rules['rules']
          after=target_rules
          # 実機設定FWルール一覧から1ルールずつ取り出し比較
          for t_before in fw_rules['rules']:
            # 実機取得ルールが、dictでなければ、エラー
            if type(t_before) != dict: module.fail_json(msg="before is not list of dict.")
            # 実機取得ルールに突合キーが存在しなければ、スキップ
            if checkkey not in t_before: continue
            # 実機取得ルールの突合キーの値を取得
            key_name=t_before[checkkey]
            #if key_name in key_name_list:
            #  module.fail_json(msg="same key_name exists in before.")
            #else:
            #  key_name_list.append(key_name)
            # 比較対象ルールから実機取得ルール突合キー値と一致する値を取得。存在しなかった場合、Addリストに追加。(新規追加ルール)
            t_after=next((x for x in target_rules if x[checkkey] == key_name), None)
            if t_after == None:
              add_item={'file_name':target_file['path'][strip_len:], 'section_name': discover_value, 'key_name' : key_name}
              add_list.append(missing_item)
              continue
            # リスト①から取得した値とリスト②から取得した値が、差分ある場合、キーで一つずつ取り出し、差分比較する
            #if t_before != t_after:
            # 実機取得設定ルールから、1要素ずつとりだし、差分比較する。
            for key  in t_before.keys():
              # 取得要素が、差分比較対象ルールに存在しないキーならスキップ
              if key not in t_after:continue
              if type(t_after[key]) == list and type(t_before[key]) != list:t_before[key] = [t_before[key]]
              if type(t_before[key]) == list and type(t_after[key]) != list:t_after[key] = [t_after[key]]
              if t_after[key] != t_before[key]:
                # 比較した差分比較対象ルールの要素がリストの場合、集合比較し、比較対象と実機設定お互いが存在しない値のみを取得する。
                if type(t_after[key]) == list:
                  t_before_exist=list(set(t_before[key]) - set(t_after[key]))
                  t_after_exist=list(set(t_after[key]) - set(t_before[key]))
                  if t_before_exist != [] or t_after_exist != []:
                    diff_item={'file_name':target_file['path'][strip_len:], 'section_name': discover_value, 'key_name' : key_name, 'key_col' : key, 'before_exist' : t_before_exist, 'after_exist' : t_after_exist}
                    diff_list.append(diff_item)
                else:
                  diff_item={'file_name':target_file['path'][strip_len:], 'section_name': discover_value, 'key_name' : key_name, 'key_col' : key, 'before_exist' : t_before[key], 'after_exist' : t_after[key]}
                  diff_list.append(diff_item)

          key_name_list=[]
          # 差分比較対象ルール一覧から1ルールずつ取り出し、実機取得ルールに存在しないルールを取得する
          for t_after in target_rules:
            # 取得した差分比較対象ルールがdict型でなければ、エラーとする
            if type(t_after) != dict: module.fail_json(msg="after is not list of dict.")
            # 取得した差分比較対象ルールに突合キーが存在しなければ、スキップ
            if checkkey not in t_after: continue
            key_name=t_after[checkkey]
            #if key_name in key_name_list:
            #  module.fail_json(msg="same key_name exists in after.")
            #else:
            #  key_name_list.append(key_name)
            # 実機取得ルールから取得した差分比較対象ルールの突合キー値と一致する値を取得。存在しなかった場合、Missingリストに追加。(実機に存在しないルール)
            t_before=next((x for x in fw_rules['rules'] if x[checkkey] == key_name), None)
            if t_before == None:
              missing_item={'file_name':target_file['path'][strip_len:], 'section_name': discover_value, 'key_name' : key_name}
              missing_list.append(add_item)
              continue
        else:
          missing_key_item={'file_name':target_file['path'][strip_len:], 'section_name': params['config_params'][checkkey]}
          missing_key_list.append(missing_key_item)

    # 結果dict: resultを作成
    result = dict(
        Add=add_list,
        Missing=missing_list,
        Change=diff_list,
        Missing_key=missing_key_list
    )

    # resultの中身を key=value,の形で出力
    module.exit_json(**result)
    
#変換処理
def convert_listofdict(module, target, target_key, target_strip, convert_list, before_key, after_key, skip_list, noconvert_failed, add_string=''):
  # 変換対象辞書リストから1要素ずつ取り出し変換を行う
  for index, t_target in enumerate(target):
    # 取り出した要素が辞書型でなければ、エラーとする
    if type(t_target) != dict: 
      module.fail_json(msg="target is not list of dict.")
    # 取り出した辞書型に変換対象キーが存在しなければ、スキップ
    if target_key not in t_target: continue
    # 変換対象値がリスト型の場合、1要素ずつ取り出し変換する 
    if type(t_target[target_key])==list:
      tmp_list=[]
      for t_target_value in t_target[target_key]:
        # 変換対象外リストに含まれる場合、変換を行わない
        if t_target_value in skip_list:
          t_value=t_target_value
        # 変換対象外リストに含まれない場合、変換参照リスト内からbefore_keyで検索し、after_keyの値に変換する。
        else:
          # t_value=next((x[after_key] for x in convert_list if x[before_key] == t_target_value.replace(target_strip,"")), None)
          t_value=None
          for x in convert_list:
            # 変換参照リスト内から取り出した値に、before_key,after_keyが含まれない場合、スキップ
            if type(x) != dict: continue 
            if before_key not in x: continue
            if after_key not in x: continue
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
      target[index][target_key]=tmp_list
    else:
      # 変換対象値がリストでない場合
      # t_value=next((x[after_key] for x in convert_list if x[before_key] == t_target[target_key].replace(target_strip,"")), None)
      t_value=None
      for x in convert_list:
        # 変換参照リスト内から取り出した値に、before_key,after_keyが含まれない場合、スキップ
        if type(x) != dict: continue
        if before_key not in x: continue
        if after_key not in x: continue
        if x[before_key] == t_target[target_key].replace(target_strip,""):
          t_value=add_string + x[after_key]
          break
      if t_value == None:
        if noconvert_failed==False:
          t_value=t_target[target_key]
        else:
          module.fail_json(msg="convart failed. " + target_key + "=" + t_target[target_key])
      target[index][target_key]=t_value
  return target

  # getapi取得
  def get_api_request(module, url, validate_certs, user, password):
    response = open_url(url=url, data=None,
                              headers={},
                              method='GET',
                              use_proxy=True, force=False,
                              last_mod_time=None,
                              timeout=300,
                              validate_certs=validate_certs,
                              url_username=user,
                              url_password=password,
                              http_agent=None,
                              force_basic_auth=True,
                              client_cert=None,
                              client_key=None,
                              ca_path=None)
      resp_code = response.getcode()
      resp_raw_data = response.read().decode('utf-8')
      resp_data = resp_raw_data
      #if resp_raw_data and is_json(resp_raw_data):
      resp_data = json.loads(resp_raw_data)
      if resp_code >= 400:
        module.fail_json(msg="API error" + url + ":code:" + resp_code)
      if resp_data is not None and 'error_code' in resp_data:
        module.fail_json(msg="API error" + url + "resp None")
    return resp_data

if __name__ == '__main__':
    main()
