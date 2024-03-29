from unicodedata import east_asian_width # 全角半角判定用
from math import isqrt
from others import Data, Embed

def check_width(string) -> int:
  "全角の文字を2文字としてカウントした文字数を返す"
  count = 0
  for char in string:
    if east_asian_width(char) in "FWA":
      count += 2
    else:
      count += 1
  return count

def get_level_up_cnt(level, chat, length):
  new_level = isqrt(chat + (length // 10))
  return new_level - level

def create_help_embed(bot):
  """
  observer help
  ---
  ヘルプで表示するembedを返す
  """
  embed = Embed.make_embed()
  for command in bot.all_commands.values():
    # 隠しコマンドは表示しない
    if command.hidden: continue
    # nameを作成
    name = bot.command_prefix + command.name
    if command.params:
      for param_name in command.params.keys():
        name += f" <{param_name}>"

    embed.add_field(name = name, value = command.brief, inline = False)

  return embed

def create_data_embed(data: Data):
  """
  observer data(-all)
  ---
  整形した表示テキストを返す
  """
  text = str()
  text += f"========== {data.name} ==========\n"
  text += f"・現在のポイント：{data.point}\n"
  text += f"・現在のレベル　：{data.level}\n"
  text += f"・合計チャット数：{data.chat}\n"
  text += f"・合計文字数　　：{data.length}\n"
  text += "="* (20 + len(data.name))

  embed = Embed.make_embed(description=text)
  return embed

def create_chat_ranking_embed(chat_data):
  """
  observer chat-ranking
  ---
  チャットランキングの表示テキストを返す
  """
  chat_data = sorted(chat_data.items(), key=lambda x:x[1], reverse=True)

  text = "===== チャット数ランキング =====\n"
  for i, (name, chat) in enumerate(chat_data):
    text += f"　第{i+1}位：{name}（{chat}回）\n"
  text += "=" * (20 + 1 + len("チャット数ランキング"))
  
  embed = Embed.make_embed(description=text)

  return embed

def create_member_list_embed(message):
  """
  observer member
  ---
  メンバー一覧の表示テキストを返す
  """
  max_string_length = 0 # 動的に[=]の文字数を変更するための変数
  text = ""             # for文で作成するテキスト
  output_text = ""      # 最終的に送信するテキスト
  
  for member in message.guild.members:
    # Botだった場合
    if member.bot: continue
    
    text += "・"
    string_length = 2 # 最初に[・]の文字数分を足す
    
    # ニックネームがなかった場合
    if member.nick == None:
      text += member.name
      string_length += check_width(member.name)
    else:
      text += member.name + "「" + member.nick + "」"
      string_length += check_width(member.name + "「" + str(member.nick) + "」")
    
    # Role があったら記述する
    role_list = [role.name for role in member.roles if role.name != "@everyone"]
    role_text = ""
    if len(role_list) != 0:
      role_text += "［"
      role_text += "  ".join(role_list)
      role_text += "］\n"
    else:
      role_text += "\n"
    
    text += role_text
    string_length += check_width(role_text)
    
    # 最大文字数を更新
    max_string_length = max(max_string_length, string_length)

  # 最大文字数が奇数だった場合偶数にする
  # これをしないと[=]の文字数が合わなくなる
  if max_string_length % 2:
    max_string_length += 1
  
  # [=]の文字数を計算
  # -14 は " メンバー一覧 " の文字数
  # // 2 は両端に [=] を付けるため
  x = (max_string_length - 13) // 2
  output_text += ("=" * x) + " メンバー一覧 " + ("=" * x) + "\n"
  output_text += text
  output_text += "=" * (max_string_length - 1)

  embed = Embed.make_embed(description=output_text)
  return embed