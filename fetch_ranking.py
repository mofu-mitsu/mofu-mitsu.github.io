import os
import json
import re
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, FilterExpression, Filter, RunReportRequest

def fetch_top_pages():
    property_id = os.environ.get("GA_PROPERTY_ID")
    if not property_id:
        raise ValueError("GA_PROPERTY_ID is not set in environment variables.")

    client = BetaAnalyticsDataClient()

    # みつきのツール完全網羅マップ
    tool_map = {
        'Wonderland-G-Tracker': {'name': 'Gモデル診断', 'desc': '最新理論「モデルG」に基づく行動観察型診断。', 'url': 'https://mofu-mitsu.github.io/Wonderland-G-Tracker/'},
        'logic-playground': {'name': 'ソシオTi強度チェッカー', 'desc': 'ソシオニクスの内的論理（Ti）に特化した精密測定ツール。', 'url': 'https://mofu-mitsu.github.io/logic-playground/'},
        'creator-brain-log': {'name': '創作16タイプ診断', 'desc': '創作活動における「情報代謝の癖」を16タイプで分析。', 'url': 'https://mofu-mitsu.github.io/creator-brain-log/'},
        'love-type-diagnosis': {'name': '恋愛4タイプ診断', 'desc': 'ソシオニクスの理論に基づき、恋愛傾向を4タイプに分類。', 'url': 'https://mofu-mitsu.github.io/love-type-diagnosis/'},
        'cognitive-dive': {'name': '認知機能ダイブ', 'desc': '行動から心理機能を測る体感型MBTI測定。', 'url': 'https://mofu-mitsu.github.io/cognitive-dive/'},
        'ideal-partner-diagnosis': {'name': '理想のソシオ恋愛診断', 'desc': 'あなたが魂レベルで求めている理想のパートナーを観測。', 'url': 'https://mofu-mitsu.github.io/ideal-partner-diagnosis/'},
        'chroma-log': {'name': 'Chroma Log / 深層心理カラー診断', 'desc': '約1658万色の中から現在の精神状態を象徴する色を抽出。', 'url': 'https://mofu-mitsu.github.io/chroma-log/'},
        'Deep-Cognition-Archive': {'name': 'Deep Cognition Archive', 'desc': '心理機能やパラメータからソシオ等を高精度で測定。', 'url': 'https://mofu-mitsu.github.io/Deep-Cognition-Archive/'},
        'model-a-builder': {'name': 'モデルA・ビルダー', 'desc': 'ソシオニクスの「モデルA」を自分の手で構築・判定。', 'url': 'https://mofu-mitsu.github.io/model-a-builder/'},
        'mbti-moyamuya': {'name': 'MBTIモヤモヤ解剖室', 'desc': '類型学への違和感を論理的に解剖。自己防衛ツール。', 'url': 'https://mofu-mitsu.github.io/mbti-moyamuya/'},
        'LII_simulator': {'name': '思考暴走シミュレーター', 'desc': '内的論理(Ti/Ni)が暴走し、思考ループに陥る体験。', 'url': 'https://mofu-mitsu.github.io/LII_simulator/'},
        'dream-code': {'name': '夢コード', 'desc': 'AIキャラと遊ぶ心理学アドベンチャー。', 'url': 'https://mofu-mitsu.github.io/dream-code/'},
        'yami_kansoku_archive': {'name': '闇観測実験アーカイブ', 'desc': 'あなたの心の奥底の闇を暴き出す。', 'url': 'https://mofu-mitsu.github.io/yami_kansoku_archive/'},
        'fluffy-love-check': {'name': 'ふわふわ相性診断', 'desc': '2人の名前を入れると相性を占うよ♡', 'url': 'https://mofu-mitsu.github.io/fluffy-love-check/'},
        'yuuki_fortune': {'name': '気まぐれ猫占い', 'desc': '猫占い師ゆうきくんが未来を鑑定🔮', 'url': 'https://mofu-mitsu.github.io/yuuki_fortune/'},
        'oshi-profile-maker': {'name': '推しキャラプロフ', 'desc': '推しの魅力を詰め込んだプロフ画像作成。', 'url': 'https://mofu-mitsu.github.io/oshi-profile-maker/'},
        'oshi-profile-maker2': {'name': '推しキャラプロフ2', 'desc': '推しの魅力を詰め込んだプロフ画像作成（Ver.2）。', 'url': 'https://mofu-mitsu.github.io/oshi-profile-maker2/'},
        'orikyara-profile-maker': {'name': 'オリキャラプロフ', 'desc': '圧倒的人気！設定画風シートが作れるメーカー。', 'url': 'https://mofu-mitsu.github.io/orikyara-profile-maker/'},
        'orikyara-profile-maker2': {'name': 'オリキャラプロフ2', 'desc': '設定画風シート作成。Ver.2。', 'url': 'https://mofu-mitsu.github.io/orikyara-profile-maker2/'},
        'Character-Student-ID-Factory': {'name': '学生証ファクトリー', 'desc': '推しやオリキャラの学生証がすぐ作れる！', 'url': 'https://mofu-mitsu.github.io/Character-Student-ID-Factory/'},
        'oshi-card-generator': {'name': '推し名刺ジェネレーター', 'desc': 'イベントやオフ会で使える推しの名刺。', 'url': 'https://mofu-mitsu.github.io/oshi-card-generator/'},
        'oshiai-card-maker': {'name': '推し愛爆発♡カード', 'desc': '推しの尊さを1枚の画像に凝縮！', 'url': 'https://mofu-mitsu.github.io/oshiai-card-maker/'},
        'oshi-date-maker': {'name': '推しとお出かけプラン', 'desc': '推しとの理想のデートプランを自動生成。', 'url': 'https://mofu-mitsu.github.io/oshi-date-maker/'},
        'Psycho-Shooter': {'name': 'Psycho-Shooter', 'desc': 'ネガティブな感情を撃ち抜くシューティング！', 'url': 'https://mofu-mitsu.github.io/Psycho-Shooter/'},
        'Torinooka-Werewolf': {'name': 'とりの丘トリ’S人狼', 'desc': 'とりの丘学園のAIキャラたちと人狼勝負！', 'url': 'https://mofu-mitsu.github.io/Torinooka-Werewolf/'},
        'world-maker': {'name': '世界観メーカー', 'desc': '創作の世界観設定をランダムに生成！', 'url': 'https://mofu-mitsu.github.io/world-maker/'},
        'orikyara-relationship-chart': {'name': '相関図メーカー', 'desc': 'キャラ同士の関係を線で整理！', 'url': 'https://mofu-mitsu.github.io/orikyara-relationship-chart/'},
        'yumekawa-dream-card': {'name': '夢日記メーカー', 'desc': '見た夢をカードにして記録しよう。', 'url': 'https://mofu-mitsu.github.io/yumekawa-dream-card/'},
        'lore-book-maker': {'name': '設定資料集ジェネレーター', 'desc': '設定を1冊のPDF資料集として出力！', 'url': 'https://mofu-mitsu.github.io/lore-book-maker/'},
        'uchinoko-check-sheet': {'name': 'うちの子観察チェック', 'desc': 'オリキャラを深く知るための質問リスト！', 'url': 'https://mofu-mitsu.github.io/uchinoko-check-sheet/'},
        'kaomoji-maker': {'name': '顔文字メーカー', 'desc': '自分だけのオリジナル顔文字を作ろう！', 'url': 'https://mofu-mitsu.github.io/kaomoji-maker/'},
        'typing-Master': {'name': 'タイピングマスター', 'desc': 'スコアアタックに挑戦してね！', 'url': 'https://mofu-mitsu.github.io/typing-Master/'},
        'kondate-maker': {'name': '献立メーカー', 'desc': 'シェフが勝手に献立を決めてくれるよ！', 'url': 'https://mofu-mitsu.github.io/kondate-maker/'}
    }

    # APIリクエスト (pagePathに修正！)
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="pagePath")],
        metrics=[Metric(name="screenPageViews")],
        date_ranges=[DateRange(start_date="30daysAgo", end_date="today")],
        dimension_filter=FilterExpression(
            not_expression=FilterExpression(
                filter=Filter(
                    field_name="pagePath",
                    in_list_filter=Filter.InListFilter(
                        values=["/", "/index.html", "/contents.html", "/about.html", "/lab.html", "/Torinooka_portal/"]
                    )
                )
            )
        ),
        limit=20
    )

    response = client.run_report(request)
    
    ranking = []
    added_keys = set()

    print("--- GA4 PV Ranking Raw Data ---")
    for row in response.rows:
        path = row.dimension_values[0].value
        print(f"Path found: {path} ({row.metric_values[0].value} PV)")
        
        # キーの抽出（末尾スラッシュや.htmlを正規化）
        key = re.sub(r'/index\.html$', '', path).strip('/')
        
        if key in tool_map and key not in added_keys:
            ranking.append(tool_map[key])
            added_keys.add(key)
            print(f"  -> Match found! Key: {key}")
        
        if len(ranking) >= 3:
            break

    # 結果を保存
    print(f"--- Final Ranking (Length: {len(ranking)}) ---")
    print(json.dumps(ranking, ensure_ascii=False, indent=2))

    with open('ranking.json', 'w', encoding='utf-8') as f:
        json.dump(ranking, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch_top_pages()
