export default function ChatMessage({ role, content }) {
  return (
    <div className={`chat-message chat-${role}`}>
      <span className="chat-role">{role === 'user' ? 'You' : 'Assistant'}</span>
      <p>{content}</p>
    </div>
  );
}
