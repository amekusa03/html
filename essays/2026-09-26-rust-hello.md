# 初めてのRust、わずか13行でGUIウィンドウを立ち上げるまで

2026-09-26 / Rust / GUI / eframe

## きっかけ

「Rustは学習コストが高い」「メモリ安全性と所有権の概念でコンパイラに怒られ続ける」──そんな評判を耳にするたび、どこか身構えてしまっていた。

しかし、近年のCLIツールや高速なデスクトップアプリの多くがRustで書かれているのを見るにつけ、いつまでも食わず嫌いをしているわけにはいかない。物は試しと、環境構築からごく小さなGUIアプリを動かすところまで、一気にやってみた。

## 環境構築

言語の導入でまずつまずきやすいのがバージョン管理とパスの設定だが、Rustはこのあたりが極めて整理されている。

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source "$HOME/.cargo/env"
```

このコマンド一発で、コンパイラ（`rustc`）だけでなく、ビルド＆パッケージ管理ツールの **`cargo`** まで一括でそろう。`cargo` はNode.jsでいう `npm` に相当するが、体験としてはもう少し気持ちがいい。

## プロジェクト作成と依存ライブラリ

開発の出発点はいつも `cargo new` だ。

```bash
cargo new hello
cd hello
```

生成された `Cargo.toml` に、GUIライブラリ **`eframe`（内部でGUIフレームワーク `egui` を使う）** を1行追加する。

```toml
[package]
name = "hello"
version = "0.1.0"
edition = "2021"

[dependencies]
eframe = "0.29"
```

次のビルド時に自動でダウンロード・コンパイルされる。この「設定ファイルに1行足すだけ」という体験の軽さは、C/C++のリンク設定と比べると隔世の感がある。

## 13行のGUI

`src/main.rs` に書いたコード全体がこれだ。

```rust
use eframe::egui;

fn main() -> eframe::Result<()> {
    let options = eframe::NativeOptions::default();

    eframe::run_simple_native("Hello App", options, move |ctx, _frame| {
        egui::CentralPanel::default().show(ctx, |ui| {
            ui.vertical_centered(|ui| {
                ui.heading("🦀 Hello Rust World! 🦀");
            });
        });
    })
}
```

`egui` は即時モード（Immediate Mode）のGUIライブラリなので、複雑なイベントループやステート管理を意識せずに、描画ツリーを素直に書き下ろせる。

あとはターミナルで叩くだけだ。

```bash
cargo run
```

初回は依存クレートのコンパイルにしばらくかかるが、2回目以降はキャッシュが効いて一瞬で起動する。ダークテーマのウィンドウが開き、中央に「🦀 Hello Rust World! 🦀」の文字が現れた瞬間は、思わず声が出た。

## 触ってみて

一番印象的だったのは **`cargo` というエコシステムの完成度** だ。プロジェクト生成からビルド・実行（`cargo run`）、エラーチェック（`cargo check`）、フォーマット（`cargo fmt`）、静的解析（`cargo clippy`）まで、すべてが1つのツールで完結する統一感がある。C/C++のような速度を持ちながら、Pythonのような手軽さでライブラリを扱える。

言語仕様のディープな部分──所有権、ライフタイム、トレイト、非同期処理──はこれから腰を据えて学んでいくことになるが、「最初の一歩」のハードルは想像より格段に低かった。

次はボタンや入力フォームを組み込んで、何か実用的なツールを作ってみようと思う。

## ソース

- [rust-hello-gui (GitHub)](https://github.com/amekusa03/rust-hello-gui)
- [eframe / egui (GitHub)](https://github.com/emilk/egui)
