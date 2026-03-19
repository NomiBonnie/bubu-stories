import { useState, useRef, useCallback, useEffect } from 'react'
import './StoryReader.css'

const BASE = import.meta.env.BASE_URL

export default function StoryReader({ story, onBack }) {
  const [page, setPage] = useState(0)
  const touchRef = useRef(null)
  const audioRef = useRef(null)
  const total = story.pages.length

  const go = useCallback((dir) => {
    setPage(p => {
      const next = p + dir
      if (next < 0) { onBack(); return p }
      if (next >= total) return p
      return next
    })
  }, [total, onBack])

  // Touch swipe
  const onTouchStart = (e) => { touchRef.current = e.touches[0].clientX }
  const onTouchEnd = (e) => {
    if (touchRef.current === null) return
    const diff = e.changedTouches[0].clientX - touchRef.current
    if (Math.abs(diff) > 50) go(diff < 0 ? 1 : -1)
    touchRef.current = null
  }

  // Click left/right half
  const onClick = (e) => {
    const x = e.clientX / window.innerWidth
    go(x > 0.5 ? 1 : -1)
  }

  // Keyboard
  useEffect(() => {
    const handler = (e) => {
      if (e.key === 'ArrowRight' || e.key === ' ') go(1)
      if (e.key === 'ArrowLeft') go(-1)
      if (e.key === 'Escape') onBack()
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [go, onBack])

  // Try to play audio
  useEffect(() => {
    const num = String(page + 1).padStart(2, '0')
    const audioSrc = `${BASE}audio/${story.date}/page-${num}.mp3`
    if (audioRef.current) {
      audioRef.current.src = audioSrc
      audioRef.current.load()
      audioRef.current.play().catch(() => {})
    }
  }, [page, story.date])

  const p = story.pages[page]
  const num = String(page + 1).padStart(2, '0')
  const imgSrc = `${BASE}images/${story.date}/page-${num}.png`

  return (
    <div
      className="reader"
      onClick={onClick}
      onTouchStart={onTouchStart}
      onTouchEnd={onTouchEnd}
    >
      <div className="reader-img-wrap">
        <img className="reader-img" src={imgSrc} alt={`Page ${page + 1}`} />
      </div>
      <div className="reader-text">
        <p>{p.text}</p>
      </div>
      <div className="reader-dots">
        {story.pages.map((_, i) => (
          <span key={i} className={`dot ${i === page ? 'active' : ''}`} />
        ))}
      </div>
      <div className="reader-page-num">{page + 1} / {total}</div>
      <audio ref={audioRef} />
    </div>
  )
}
