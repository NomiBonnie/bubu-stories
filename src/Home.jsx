import './Home.css'

const BASE = import.meta.env.BASE_URL

export default function Home({ stories, onSelect }) {
  return (
    <div className="home">
      <h1 className="home-header">咘咘的故事书 ✨</h1>
      <div className="stories-grid">
        {stories.map(s => {
          const coverImg = `${BASE}images/${s.id}/${s.cover}.png`
          return (
            <div key={s.id} className="story-card" onClick={() => onSelect(s.id)}>
              <div className="story-card-img-wrap">
                <img src={coverImg} alt={s.title} className="story-card-img" />
              </div>
              <div className="story-card-info">
                <h2 className="story-card-title">{s.title}</h2>
                <p className="story-card-meta">{s.date} · {s.pages}页</p>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
