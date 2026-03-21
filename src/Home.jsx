import './Home.css'

const BASE = import.meta.env.BASE_URL

export default function Home({ stories, onSelect }) {
  return (
    <div className="home">
      <h1 className="home-header">Bubu's Stories</h1>
      <p className="home-subtitle">咘咘的睡前故事</p>
      <div className="home-divider" />
      <div className="stories-grid">
        {stories.map(s => {
          const coverImg = `${BASE}images/${s.id}/${s.cover}.jpg`
          return (
            <div key={s.id} className="story-card" onClick={() => onSelect(s.id)}>
              <div className="story-card-info">
                {s.chapter && <p className="story-card-chapter">Chapter {s.chapter}</p>}
                <h2 className="story-card-title">{s.title}</h2>
              </div>
              <div className="story-card-img-wrap">
                <img src={coverImg} alt={s.title} className="story-card-img" />
              </div>
              {s.tags && (
                <p className="story-card-tags">{s.tags.join('  ·  ')}</p>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
