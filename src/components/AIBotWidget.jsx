import { useState, useCallback, useEffect, useRef } from "react";

export default function AIBotWidget({ history = [] }) {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      id: "welcome",
      from: "bot",
      text: "Hi 👋 I’m your AI Fitness Coach.\nAsk me anything!"
    }
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Auto scroll to bottom
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  const sendMessage = async (msgOverride) => {
    const text = (msgOverride ?? input).trim();
    if (!text || isLoading) return;

    const userMsg = {
      id: `user-${Date.now()}`,
      from: "user",
      text
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: text,
          history: [...history, ...messages, userMsg]
        })
      });

      if (!res.ok) throw new Error("Server error");

      const data = await res.json();

      setMessages((prev) => [
        ...prev,
        {
          id: `bot-${Date.now()}`,
          from: "bot",
          text: data.reply || "Sorry, I didn't get that. Try again!"
        }
      ]);
    } catch (e) {
      setMessages((prev) => [
        ...prev,
        {
          id: `error-${Date.now()}`,
          from: "bot",
          text:
            "⚠️ I’m having trouble reaching my brain. Check if the server is running and try again."
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      {/* Floating Button */}
      {!open && (
        <button
          onClick={() => setOpen(true)}
          aria-label="Open AI Fitness Coach"
          className="fixed bottom-6 right-6 rounded-full p-4
            bg-gradient-to-r from-[#a4f16c] to-[#7ed321]
            shadow-[0_14px_40px_rgba(148,255,120,0.55)]
            hover:scale-105 active:scale-95
            transition-all duration-200 z-50
            flex items-center justify-center"
        >
          <span className="text-2xl">🤖</span>
        </button>
      )}

      {/* Chat Window */}
      {open && (
        <div
          className="fixed bottom-6 right-6 w-96 max-w-[95vw] h-[520px]
            bg-slate-900/95 backdrop-blur-xl
            border border-slate-700/70
            rounded-3xl shadow-[0_22px_60px_rgba(0,0,0,0.85)]
            flex flex-col overflow-hidden z-50
            animate-[fadeIn_0.2s_ease-out]"
        >
          {/* Header */}
          <div className="p-4 bg-gradient-to-r from-slate-900 to-slate-800 border-b border-slate-700/70 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="relative">
                <div className="w-9 h-9 rounded-full bg-[#a4f16c] flex items-center justify-center text-xl">
                  🤖
                </div>
                <span className="w-2.5 h-2.5 bg-emerald-400 rounded-full border-2 border-slate-900 absolute -right-0.5 -bottom-0.5" />
              </div>
              <div className="flex flex-col">
                <span className="text-sm font-semibold">AI Fitness Coach</span>
                <span className="text-[11px] text-slate-400">
                  Personalised workouts & recovery tips
                </span>
              </div>
            </div>
            <button
              onClick={() => setOpen(false)}
              aria-label="Close chat"
              className="text-slate-400 hover:text-white hover:bg-slate-700/60 rounded-full p-1.5 transition"
            >
              ✕
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 p-4 space-y-3 overflow-y-auto text-sm">
            {messages.map((m) => (
              <div
                key={m.id}
                className={`max-w-[88%] px-3.5 py-2.5 rounded-2xl whitespace-pre-line leading-relaxed
                  ${
                    m.from === "bot"
                      ? "bg-slate-800/90 text-emerald-200 border border-slate-700/70 shadow-lg shadow-emerald-900/30"
                      : "bg-[#a4f16c] text-black ml-auto shadow-lg shadow-lime-500/30"
                  }`}
              >
                {m.text}
              </div>
            ))}

            {isLoading && (
              <div className="inline-flex items-center gap-2 max-w-[75%] px-3.5 py-2.5 rounded-2xl bg-slate-800/90 text-emerald-200 border border-slate-700/70">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-300 animate-bounce [animation-delay:-0.2s]" />
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-300 animate-bounce [animation-delay:-0.1s]" />
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-300 animate-bounce" />
                <span className="text-[11px] text-emerald-100/80 ml-1">
                  Thinking…
                </span>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Quick Replies */}
          <div className="px-3 pb-2 flex flex-wrap gap-2 border-t border-slate-800/80 bg-slate-900/60">
            {[
              "What should I train tomorrow?",
              "Suggest a weekly plan",
              "Am I overtraining?",
              "Give me a quick home workout",
              "Diet tips for fat loss"
            ].map((q, i) => (
              <button
                key={i}
                onClick={() => sendMessage(q)}
                disabled={isLoading}
                className="text-[11px] px-3 py-1.5 rounded-full
                  bg-slate-800/80 border border-slate-700/80
                  text-slate-200 hover:bg-slate-700/80
                  transition disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {q}
              </button>
            ))}
          </div>

          {/* Input */}
          <div className="p-3 border-t border-slate-800/80 bg-slate-950/80">
            <div className="flex items-center gap-2">
              <input
                className="flex-1 px-3 py-2 rounded-full bg-slate-900/80 text-sm
                  placeholder:text-slate-500 text-slate-100
                  outline-none border border-slate-700/70
                  focus:ring-2 focus:ring-[#a4f16c]/50 focus:border-transparent
                  transition"
                placeholder="Ask about workouts, nutrition, or recovery…"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                  }
                }}
                disabled={isLoading}
              />
              <button
                onClick={() => sendMessage()}
                disabled={!input.trim() || isLoading}
                className="px-4 py-2 rounded-full bg-gradient-to-r from-[#a4f16c] to-[#7ed321]
                  text-black text-xs font-semibold
                  hover:scale-105 active:scale-95
                  disabled:opacity-50 disabled:cursor-not-allowed
                  shadow-md shadow-lime-500/40 transition"
              >
                {isLoading ? "..." : "Send"}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
