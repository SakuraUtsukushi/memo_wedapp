// フロントエンド
import React, { useState, useEffect } from "react";
import axios from "axios";

// python 開発環境の情報
const API_URL = "http://localhost:8000";

function App() {
  const [memos, setMemos] = useState([]);
  const [title, setTitle] = useState("");
  const [status, setStatus] = useState("");
  const [content, setContent] = useState("");
  const [editingId, setEditingId] = useState(null);
  const [editTitle, setEditTitle] = useState("");
  const [editContent, setEditContent] = useState("");
  const [editStatus, setEditStatus] = useState("");

  // メモ一覧取得
  const fetchMemos = () => {
    fetch(`${API_URL}/memos`)
      .then(res => res.json())
      .then(data => setMemos(data))
      .catch(err => console.error("Fetch error:", err));
  };

  useEffect(() => {
    fetchMemos();
  }, []);

  // 新規メモ追加
  const addMemo = () => {
    if (!title.trim() || !content.trim()) {
      alert("タイトルと内容を入力してください");
      return;
    }

    fetch(`${API_URL}/memos/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title: title,
        content: content,
        status: "未完了"  // 初期ステータスを固定
      })
    })
      .then(res => {
        if (!res.ok) throw new Error("登録に失敗しました");
        return res.json();
      })
      .then(memo => {
        setMemos([...memos, memo]);
        setTitle("");
        setContent("");
        setStatus(""); // フォームの状態はリセット
      })
      .catch(err => console.error("追加エラー:", err));
  };

// 編集開始
  const startEdit = (memo) => {
    setEditingId(memo.id);
    setEditTitle(memo.title);
    setEditStatus(memo.status);
    setEditContent(memo.content);
  };

  // 保存
  const saveEdit = () => {
    if (!editTitle.trim() || !editContent.trim()) {
      alert("タイトルと内容を入力してください");
      return;
    }
    fetch(`${API_URL}/memos/${editingId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title: editTitle,
        content: editContent,
        status: editStatus
      })
    })
      .then(res => res.json())
      .then(() => {
        setEditingId(null);
        setEditTitle("");
        setEditContent("");
        setEditStatus("");
        fetchMemos();
      })
      .catch(err => alert(err.message));
  };

  // メモ削除
  const deleteMemo = (id) => {
    axios.delete(`${API_URL}/memos/${id}`)
      .then(() => setMemos(memos.filter(m => m.id !== id)))
      .catch(err => console.error(err));
  };

  return (
    <div style={{ padding: "20px", fontFamily: "sans-serif" }}>
    <h1>メモ帳</h1>
    <input
      placeholder="タイトル（最大100文字）"
      value={title}
      onChange={e => {
        const value = e.target.value;
        if (value.length <= 100) {  // DBに合わせ100文字に制限
          setTitle(value);
        }
      }}
      style={{ width: "300px", marginBottom: "5px" }}
    /><br/>
    <textarea
      placeholder="内容（最大255文字）"
      value={content}
      onChange={e => {
        const value = e.target.value;
        if (value.length <= 255) {  // DBに合わせ255文字に制限　改行も文字数に含まれる
          setContent(value);
        }
      }}
      rows={5}
      cols={40}
      style={{ width: "300px", height: "100px", marginBottom: "5px" }}
    /><br />
      
    {/* ステータスの表示 */}
    <select value={status} onChange={e => setStatus(e.target.value)}>
    <option value="未完了">未完了</option>
    <option value="完了">完了</option>
    </select>
    <button onClick={addMemo}>保存</button><br/><br/>

    {/* メモ一覧 */}
    {memos.map((memo) => (
      <div key={memo.id} style={{
        border: "2px solid #ccc",
        padding: "10px",
        marginBottom: "10px",
        whiteSpace: "pre-wrap", //改行と空白を維持
      }}>
      {editingId === memo.id ? (
      <>
      <input
        type="text"
        placeholder="タイトル（最大100文字）"
        value={editTitle}
        onChange={e => {
          const value = e.target.value;
          if (value.length <= 100) {  // DBに合わせ100文字に制限
            setEditTitle(e.target.value);
          }
        }}
        style={{ display: "block", marginBottom: "5px" }}
      />
      <textarea
        placeholder="内容（最大255文字）"
        value={editContent}
        onChange={e => {
          const value = e.target.value;
          if (value.length <= 255) {  // DBに合わせ255文字に制限　改行も文字数に含まれる
            setEditContent(e.target.value);
          }
        }}
        style={{ display: "block", marginBottom: "5px" }}
      />
      <select
        value={editStatus}
        onChange={e => setEditStatus(e.target.value)}
      >
      <option value="未完了">未完了</option>
      <option value="完了">完了</option>
      </select><br/>

      <button onClick={saveEdit}>保存</button>
      <button
        onClick={() => setEditingId(null)}
        style={{ marginLeft: "5px" }}>キャンセル</button>
      </>
      ) : (
        <>
        <h3>{memo.title}</h3>
        <p>{memo.content}</p>
        <p>{memo.status}</p>
        <small>作成日：{new Date(memo.created_at).toLocaleString()}｜</small>
        <small>更新日: {
          (() => {
            if (!memo.updated_at) return "";
              const dateObj = new Date(memo.updated_at);
              return isNaN(dateObj.getTime())
              ? ""
              : dateObj.toLocaleString();
          })()
        }</small>
        <br/>
        <button onClick={() => startEdit(memo)}>編集</button>
        <button onClick={() => deleteMemo(memo.id)} style={{ marginLeft: "5px" }}>削除</button>
        </>
      )}
      </div>
    ))}
    </div>
  );
}

export default App;