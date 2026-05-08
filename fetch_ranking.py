import os
import json
import re
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, FilterExpression, FilterExpressionList, DimensionFilter, Filter

def fetch_top_pages():
    # 環境変数からプロパティIDを取得
    property_id = os.environ.get("GA_PROPERTY_ID")
    if not property_id:
        raise ValueError("GA_PROPERTY_ID is not set in environment variables.")

    client = BetaAnalyticsDataClient()

    # みつきのツール完全網羅マップ
    tool_map = {
        'dream-code': {'name': '夢コード', 'desc': 'AIキャラと戦う心理学アドベンチャー。', 'path': 'https://mofu-mitsu.github.io/dream-code/'},
        'model-a-builder': {'name': 'モデルA・ビルダー', 'desc': 'ソシオニクスの「モデルA」を構築・判定。', 'path': 'https://mofu-mitsu.github.io/model-a-builder/'},
        'mbti-moyamuya': {'name': 'MBTIモヤモヤ解剖室', 'desc': '類型学への違和感を論理的に解剖。', 'path': 'https://mofu-mitsu.github.io/mbti-moyamuya/'},
        'LII_simulator': {'name': '思考暴走シミュレーター', 'desc': 'LII/INTJの脳内メモリの限界を追体験。', 'path': 'https://mofu-mitsu.github.io/LII_simulator/'},
        'Deep-Cognition-Archive': {'name': 'Deep Cognition Archive', 'desc': '心理機能から深層タイプを精密に観測。', 'path': 'https://mofu-mitsu.github.io/Deep-Cognition-Archive/'},
        'yami_kansoku_archive': {'name': '闇観測実験アーカイブ', 'desc': 'あなたの心の奥底の闇を暴き出す。', 'path': 'https://mofu-mitsu.github.io/yami_kansoku_archive/'},
        'fluffy-love-check': {'name': 'ふわふわ相性診断', 'desc': '2人の名前を入れると相性を占うよ♡', 'path': 'https://mofu-mitsu.github.io/fluffy-love-check/'},
        'yuuki_fortune': {'name': '気まぐれ猫占い', 'desc': '猫占い師ゆうきくんが未来を鑑定🔮', 'path': 'https://mofu-mitsu.github.io/yuuki_fortune/'},
        'oshi-profile-maker': {'name': '推しキャラプロフ', 'desc': '推しの魅力を詰め込んだプロフ画像作成。', 'path': 'https://mofu-mitsu.github.io/oshi-profile-maker/'},
        'oshi-profile-maker2': {'name': '推しキャラプロフ2', 'desc': '推しの魅力を詰め込んだプロフ画像作成。', 'path': 'https://mofu-mitsu.github.io/oshi-profile-maker2/'},
        'orikyara-profile-maker2': {'name': 'オリキャラプロフ2', 'desc': '圧倒的人気！うちの子の魅力を1枚に。', 'path': 'https://mofu-mitsu.github.io/orikyara-profile-maker2/'}, # オリキャラプロフ2が人気なので見出しを調整
        'orikyara-profile-maker': {'name': 'オリキャラプロフ', 'desc': '圧倒的人気！設定画風シートが作れるメーカー。', 'path': 'https://mofu-mitsu.github.io/orikyara-profile-maker/'},
        'Character-Student-ID-Factory': {'name': '学生証ファクトリー', 'desc': '推しやオリキャラの学生証がすぐ作れる！', 'path': 'https://mofu-mitsu.github.io/Character-Student-ID-Factory/'},
        'oshi-card-generator': {'name': '推し名刺ジェネレーター', 'desc': 'イベントやオフ会で使える推しの名刺。', 'path': 'https://mofu-mitsu.github.io/oshi-card-generator/'},
        'oshiai-card-maker': {'name': '推し愛爆発♡カード', 'desc': '推しの尊さを1枚の画像に凝縮！', 'path': 'https://mofu-mitsu.github.io/oshiai-card-maker/'},
        'oshi-date-maker': {'name': '推しとお出かけプラン', 'desc': '推しとの理想のデートプランを自動生成。', 'path': 'https://mofu-mitsu.github.io/oshi-date-maker/'},
        'Psycho-Shooter': {'name': 'Psycho-Shooter', 'desc': 'ネガティブな感情を撃ち抜くシューティング！', 'path': 'https://mofu-mitsu.github.io/Psycho-Shooter/'},
        'Torinooka-Werewolf': {'name': 'とりの丘トリ’S人狼', 'desc': 'とりの丘学園のAIキャラたちと人狼勝負！', 'path': 'https://mofu-mitsu.github.io/Torinooka-Werewolf/'},
        'world-maker': {'name': '世界観メーカー', 'desc': '創作の世界観設定をランダムに生成！', 'path': 'https://mofu-mitsu.github.io/world-maker/'},
        'orikyara-relationship-chart': {'name': '相関図メーカー', 'desc': 'キャラ同士の関係を線で整理！', 'path': 'https://mofu-mitsu.github.io/orikyara-relationship-chart/'},
        'yumekawa-dream-card': {'name': '夢日記メーカー', 'desc': '見た夢をカードにして記録しよう。', 'path': 'https://mofu-mitsu.github.io/yumekawa-dream-card/'},
        'uchinoko-check-sheet': {'name': 'うちの子観察チェック', 'desc': 'オリキャラを深く知るための質問リスト！', 'path': 'https://mofu-mitsu.github.io/uchinoko-check-sheet/'},
        'kaomoji-maker': {'name': '顔文字メーカー', 'desc': '自分だけのオリジナル顔文字を作ろう！', 'path': 'https://mofu-mitsu.github.io/kaomoji-maker/'},
        'typing-Master': {'name': 'タイピングマスター', 'desc': 'スコアアタックに挑戦してね！', 'path': 'https://mofu-mitsu.github.io/typing-Master/'},
        'kondate-maker': {'name': '献立メーカー', 'desc': 'シェフが勝手に献立を決めてくれるよ！', 'path': 'https://mofu-mitsu.github.io/kondate-maker/'}
    }

    # APIリクエスト（直近30日のPVが多いページを抽出）
    request = {
        "property": f"properties/{property_id}",
        "dimensions":[Dimension(name="pagePath")],
        "metrics": [Metric(name="screenPageViews")],
        "date_ranges":[DateRange(start_date="30daysAgo", end_date="today")],
        "limit": 20
    }

    response = client.run_report(request)
    
    ranking =[]
    added_keys = set()

    for row in response.rows:
        path = row.dimension_values[0].value
        # 余計なスラッシュやindex.htmlを取り除く
        key = re.sub(r'/index\.html$', '', path).strip('/')
        
        if key in tool_map and key not in added_keys:
            ranking.append(tool_map[key])
            added_keys.add(key)
        
        if len(ranking) >= 3:
            break

    # JSONファイルに保存
    with open('ranking.json', 'w', encoding='utf-8') as f:
        json.dump(ranking, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch_top_pages()
