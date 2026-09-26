# Getting Started with Rust: Launching a GUI Window in Just 13 Lines of Code

2026-09-26 / Rust / GUI / eframe

## chance

“Rust has a steep learning curve,” “The compiler keeps scolding you over memory safety and ownership”—whenever I heard comments like that, I found myself bracing for the worst.

However, seeing how many recent CLI tools and high-performance desktop apps are written in Rust, I realized I couldn’t keep avoiding it indefinitely. Figuring I might as well give it a try, I went ahead and did everything in one go—from setting up the environment to running a very simple GUI app.

## Setting Up the Environment

When getting started with a new programming language, version control and path configuration are often the first stumbling blocks, but Rust handles these aspects extremely well.

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source "$HOME/.cargo/env"
```

With just this one command, you can set up not only the compiler (`rustc`) but also the build and package management tools **`cargo`** all at once. `cargo` is equivalent to `npm` in Node.js, but it feels a bit smoother in practice.

## Creating a Project and Dependency Libraries

The starting point for development is always `cargo new`.

```bash
cargo new hello
cd hello
```

Add one line for the GUI library **`eframe` (which uses the GUI framework `egui` internally)** to the generated `Cargo.toml`.

```toml
[package]
name = "hello"
version = "0.1.0"
edition = "2021"

[dependencies]
eframe = "0.29"
```

It will be automatically downloaded and compiled during the next build. The ease of this process—simply adding a single line to the configuration file—feels like a world of difference compared to C/C++ linker settings.

## 13-line GUI

This is the entire code I wrote in `src/main.rs`.

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

Since `egui` is an Immediate Mode GUI library, you can easily construct the rendering tree without having to worry about complex event loops or state management.

All that's left is to type it into the terminal.

```bash
cargo run
```

The first time, it takes a while to compile the dependency crates, but from the second time onward, the cache kicks in and it launches instantly. When the dark-theme window opened and the text “🦀 Hello Rust World! 🦀” appeared in the center, I couldn’t help but let out a gasp.

## Give it a try

What impressed me the most was **the level of polish in the **`cargo`** ecosystem**. From project creation to building and execution (`cargo run`), error checking (`cargo check`), formatting (`cargo fmt`), and static analysis (`cargo clippy`), everything is handled within a single tool, creating a sense of cohesion. It allows you to work with libraries with the speed of C/C++ and the ease of Python.

I’ll be taking the time to thoroughly study the deeper aspects of the language specification—ownership, lifetimes, traits, and asynchronous processing—but the hurdle for taking that “first step” was significantly lower than I had imagined.

Next, I'm thinking of incorporating buttons and input forms to try making a practical tool.

## sauce

- [rust-hello-gui (GitHub)](https://github.com/amekusa03/rust-hello-gui)
- [eframe / egui (GitHub)](https://github.com/emilk/egui)
