# Shelper

openrouterを使ったコマンドヘルパー

# Example

```bash
$ shelper CPUの情報を取得してまとめて
shelper needs to execute command: lscpu
Do you want to execute? (y/n): y
shelper needs to execute command: mpstat -P ALL
Do you want to execute? (y/n): y
shelper needs to execute command: sensors
Do you want to execute? (y/n): y
CPUの情報を収集しました。以下にまとめてご報告します。

## CPU基本情報
- **モデル**: 12th Gen Intel Core i5-1250P
- **アーキテクチャ**: x86_64
- **物理コア数**: 12コア
- **論理CPU数**: 16 (Hyper-Threading有効)
- **スレッド/コア**: 2
- **周波数範囲**: 400 MHz 〜 4.4 GHz
- **現在の周波数スケーリング**: 49%

## キャッシュ情報
- **L1データキャッシュ**: 448 KiB (12インスタンス)
- **L1命令キャッシュ**: 640 KiB (12インスタンス)
- **L2キャッシュ**: 9 MiB (6インスタンス)
- **L3キャッシュ**: 12 MiB (1インスタンス)

## 現在のCPU使用状況
- **全体平均**: アイドル状態 90.78%、ユーザ空間 5.77%、システム空間 2.71%
- **最も使用率が高いコア**: CPU6 (アイドル状態 84.23%)
- **最も使用率が低いコア**: CPU11 (アイドル状態 93.32%)

## 温度情報
- **CPUパッケージ**: 72.0°C (上限: 100.0°C)
- **最も温度が高いコア**: Core 0 (72.0°C)
- **最も温度が低いコア**: 複数のコアが 63.0°C
- **ThinkPadセンサー**: CPU 68.0°C、ファン回転数 3073 RPM

このCPUはIntelの第12世代Core i5プロセッサで、高性能コアと高効率コアの組み合わせを持つハイブリッド設計の可能性があります。現在は比較的高めの負荷状態と温度を示していますが、すべて正常範囲内です。
meta { model: anthropic/claude-3.7-sonnet:thinking, input: 4362, output: 1033, cost: 0.028581$ }
...
```

# Install

```bash
git clone https://this/repo.git
uv tool install . -e
```

# TODO

- モデル選択
- MCP機能
- もうちょっと沢山の情報を吸い出してやったほうが良さそう
- 対話機能つけるべきやね
