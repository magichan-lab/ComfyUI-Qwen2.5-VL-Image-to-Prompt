# ComfyUI 用 Qwen2.5-VL Image to Prompt

[English README](README.md)

入力画像から、ローカルで動作する [Qwen2.5-VL-3B-Instruct](https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct) を使って、英語の画像生成用プロンプトを作成します。このリポジトリには、ComfyUI のカスタムノード 1 個と、生成したプロンプトから試作画像をプレビューできるワークフローのサンプルが含まれます。カスタムノード単体は画像を生成しません。

## 機能

- ComfyUI の `IMAGE` を受け取り、画像に見える内容を画像生成用のテキストプロンプトとして記述します。
- 指示文、末尾に追加するプロンプト、モデル ID、最大出力トークン数を編集できます。
- 生成したテキストをノード内に表示し、後続ノードで使える `STRING` 出力として渡します。
- 入力が複数画像のバッチの場合は、最初の画像を使用します。

初回使用時には、既定のモデルを Hugging Face からダウンロードし、Transformers がキャッシュします。モデルの重みはこのリポジトリには含まれません。CUDA 対応 GPU の使用を推奨します。CPU でも推論できますが、処理が遅く、十分なメモリが必要です。モデルの重みには、そのモデル固有のライセンスと利用条件が適用されます。

## インストール

### ComfyUI Manager を使う場合

このパッケージが [Comfy Registry](https://registry.comfy.org/) に公開された後は、ComfyUI Manager で **Qwen2.5-VL Image to Prompt** を検索してインストールしてください。インストール後、ComfyUI を再起動します。

Registry に掲載されるまでは、利用中の Manager に Git URL からのインストール機能があればそれを使うか、以下の手順で手動インストールしてください。

### 手動インストール

ComfyUI のインストール先で、次のコマンドを実行します。

```bash
cd custom_nodes
git clone https://github.com/magichan-lab/ComfyUI-Qwen2.5-VL-Image-to-Prompt.git
cd ComfyUI-Qwen2.5-VL-Image-to-Prompt
python -m pip install -r requirements.txt
```

`pip` コマンドには、ComfyUI の実行に使っている Python 環境を使用し、その後 ComfyUI を再起動してください。PyTorch と NumPy は ComfyUI 側から提供されます。このパッケージで追加する依存関係は [`requirements.txt`](requirements.txt) に記載されています。

## サンプルワークフローの使い方

1. ComfyUI で [`workflows/qwen25vl_image_to_prompt.json`](workflows/qwen25vl_image_to_prompt.json) を開きます。
2. **Load Image** で、ComfyUI の input ディレクトリ内の画像を選択します。設定済みの `example.png` は仮のファイル名で、画像ファイルは同梱されていません。
3. **Load Checkpoint** で、ComfyUI の `models/checkpoints` にある画像生成用チェックポイントを選択します。設定済みの `select_your_checkpoint.safetensors` は仮のファイル名です。`model_id` で指定する Qwen2.5-VL とは別のモデルが必要です。
4. ワークフローを実行します。生成された `final_prompt` がポジティブプロンプトに渡され、**Preview Image** に試作画像が表示されます。必要なら **Negative prompt (optional)** に避けたい要素を入力します。
5. 元画像と試作画像を見比べ、**Qwen2.5-VL Image to Prompt** の指示文や `append_prompt` を編集して再実行します。比較中は **KSampler** のシードを `fixed` のままにすると、プロンプトの変更による差を確認しやすくなります。

既定の指示文では、画像に見える内容だけを記述するよう求めています。画像の説明には抜けや誤りが生じる場合があるため、生成されたプロンプトを確認してください。`model_id` 欄は、互換性のある Qwen2.5-VL チェックポイントを指定するためのものです。サンプルの試作画像は 512 × 512 ピクセルです。使用する画像生成チェックポイントに合わせて **Empty Latent Image** のサイズや **KSampler** の設定を調整してください。**Preview Image** は画像を永続保存しません。保存したい場合は **Save Image** ノードを追加してください。

## リポジトリの構成

```text
.
├── __init__.py                 # ComfyUI ノードのエントリーポイント
├── nodes.py                    # ノードの実装
├── requirements.txt            # Manager がインストールする依存関係
├── pyproject.toml              # Comfy Registry のメタデータ
├── workflows/
│   └── qwen25vl_image_to_prompt.json
├── LICENSE
├── README.md
└── README.ja.md
```

現在のノード ID は `Qwen25VLImageToPrompt` です。以前の `Krea2ImageToPrompt` も互換用の別名として残しているため、既存のワークフローを読み込めます。

## ComfyUI Manager で公開する前に

1. [magichan-lab/ComfyUI-Qwen2.5-VL-Image-to-Prompt](https://github.com/magichan-lab/ComfyUI-Qwen2.5-VL-Image-to-Prompt) のルートに、これらのファイルをプッシュします。
2. [Comfy Registry](https://registry.comfy.org/) でパブリッシャーを作成し、`pyproject.toml` の `YOUR_PUBLISHER_ID` を正確な ID に置き換えます。Registry ID に空きがあれば、パッケージ名は `qwen25vl-image-to-prompt` のままにします。Registry のノード名は作成後に変更できません。
3. `comfy node publish` または Registry が対応する GitHub Actions ワークフローでバージョンを公開します。Manager は Registry を通じて公開済みノードを検出します。詳しくは[公式の公開ガイド](https://docs.comfy.org/registry/publishing)を参照してください。

従来の Manager の一覧に登録する場合は、[Manager の登録ガイド](https://docs.comfy.org/custom-nodes/backend/manager)に従い、`custom-node-list.json` にリポジトリ URL を追加するプルリクエストを送ります。このリポジトリは登録に向けて準備されていますが、まだ登録・公開されていません。

## ライセンス

カスタムノードのコードとワークフローには [MIT License](LICENSE) が適用されます。Qwen2.5-VL のモデルの重みは別途配布され、それぞれの利用条件が適用されます。
