import React from 'react'
import {useState, useEffect} from 'react'

const messages =[
    "Seeding fresh jobs...",
    "Scanning through 500+ companies...",
    "Crunching the numbers...",
    "Almost there..."

]


const RotatingLoadingMessage = () => {
    const[index, setIndex] = useState(0)

    useEffect(()=>{
        const interval = setInterval(()=>{
            setIndex((prev) => (prev + 1) % messages.length)
        }, 3000) // 3000 ms before updating

        return () => clearInterval(interval)

    },[])



  return (
    <div>
      <p className="text-gray-500 text-sm animate-pulse">{messages[index]}</p>
    </div>
  )
}

export default RotatingLoadingMessage
