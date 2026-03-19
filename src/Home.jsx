import './Home.css'

export default function Home({ story, onStart }) {
  return (
    <div className="home" onClick={onStart}>
      <div className="home-card">
        <div className="home-icon">🐰</div>
        <h1 className="home-title">{story.title}</h1>
        <p className="home-date">{story.date}</p>
        <div className="home-hint">点击开始阅读</div>
      </div>
      <div className="home-footer">咘咘的故事书 ✨</div>
    </div>
  )
}
