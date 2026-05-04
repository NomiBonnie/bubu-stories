// Build timestamp: 2026-04-24 23:53
import { useState, useRef, useCallback, useEffect } from 'react'
import './StoryReader.css'

const BASE = import.meta.env.BASE_URL

function imgUrl(id, pageNum) {
  const buildTime = '20260425-1230'; // Force bundle rehash
  return `${BASE}images/${id}/page-${String(pageNum).padStart(2, '0')}.jpg?v=${buildTime}`
}

export default function StoryReader({ story, storyId, onBack, lang, toggleLang }) {
  const [page, setPage] = useState(0)
  const touchRef = useRef(null)
  const readerRef = useRef(null)
  const total = story.pages.length

  // Disable pinch-to-zoom on iOS Safari
  useEffect(() => {
    const prevent = (e) => { if (e.touches && e.touches.length > 1) e.preventDefault() }
    document.addEventListener('touchmove', prevent, { passive: false })
    // Also prevent gesturestart (Safari specific)
    const preventGesture = (e) => e.preventDefault()
    document.addEventListener('gesturestart', preventGesture, { passive: false })
    document.addEventListener('gesturechange', preventGesture, { passive: false })
    return () => {
      document.removeEventListener('touchmove', prevent)
      document.removeEventListener('gesturestart', preventGesture)
      document.removeEventListener('gesturechange', preventGesture)
    }
  }, [])

  // Scroll to top on page change
  useEffect(() => {
    if (readerRef.current) readerRef.current.scrollTop = 0
  }, [page])

  const go = useCallback((dir) => {
    setPage(p => {
      const next = p + dir
      if (next < 0) { onBack(); return p }
      if (next >= total) return p
      return next
    })
  }, [total, onBack])

  // Preload next 2 images
  useEffect(() => {
    for (let i = 1; i <= 2; i++) {
      const next = page + i
      if (next < total) {
        const img = new Image()
        img.src = imgUrl(storyId, next + 1)
      }
    }
  }, [page, total, storyId])

  const onTouchStart = (e) => {
    if (e.touches.length > 1) return // ignore multi-touch
    touchRef.current = { x: e.touches[0].clientX, y: e.touches[0].clientY }
  }
  const onTouchEnd = (e) => {
    if (touchRef.current === null) return
    const dx = e.changedTouches[0].clientX - touchRef.current.x
    const dy = e.changedTouches[0].clientY - touchRef.current.y
    // Only swipe if horizontal movement > vertical (not scrolling)
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) go(dx < 0 ? 1 : -1)
    touchRef.current = null
  }

  const onClick = (e) => {
    const x = e.clientX / window.innerWidth
    go(x > 0.5 ? 1 : -1)
  }

  useEffect(() => {
    const handler = (e) => {
      if (e.key === 'ArrowRight' || e.key === ' ') go(1)
      if (e.key === 'ArrowLeft') go(-1)
      if (e.key === 'Escape') onBack()
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [go, onBack])

  const p = story.pages[page]
  const imgSrc = imgUrl(storyId, page + 1)

  return (
    <div
      className="reader"
      ref={readerRef}
      onClick={onClick}
      onTouchStart={onTouchStart}
      onTouchEnd={onTouchEnd}
    >
      <button className="reader-back" onClick={(e) => { e.stopPropagation(); onBack() }}>←</button>
      <button className="reader-lang" onClick={(e) => { e.stopPropagation(); toggleLang() }}>{lang === 'zh' ? 'EN' : '中'}</button>
      <img className="reader-img" src={imgSrc} alt={`Page ${page + 1}`} />
      <div className="reader-text">
        <p>{lang === 'en' ? (p.text_en || p.text) : p.text}</p>
      </div>
      <div className="reader-dots">
        {story.pages.map((_, i) => (
          <span key={i} className={`dot ${i === page ? 'active' : ''}`} />
        ))}
      </div>
      <div className="reader-page-num">{page + 1} / {total}</div>
    </div>
  )
}
