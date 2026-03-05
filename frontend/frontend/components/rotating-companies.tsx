'use client';

import React, { useEffect, useState } from 'react'
import BlurText from './BlurText'


/*
const logos =[

  "Stripe",
  "Amazon",
  "Walmart"
]
*/

const logos = [
  "/company-logos/stripe.svg",
  "/company-logos/duolingo.svg",
  "/company-logos/cloudflare.svg",
  "/company-logos/roku.svg",
  "/company-logos/lyft.svg",
  "/company-logos/chime.svg",
  "/company-logos/figma.svg",

]


type RotatingCompaniesProps = {
  startOffset?: number;
};

const RotatingCompanies = ({ startOffset = 0 }: RotatingCompaniesProps) => {
  const [index, setIndex] = useState(0)
  const safeLogos = logos.filter(Boolean)
  const normalizedOffset =
    safeLogos.length > 0 ? ((startOffset % safeLogos.length) + safeLogos.length) % safeLogos.length : 0
  const currentLogo = safeLogos.length > 0 ? safeLogos[index % safeLogos.length] : null
  
  useEffect(()=>{
    if (safeLogos.length === 0) return;

    setIndex(normalizedOffset);

    const interval = setInterval(()=>{
      setIndex((prev) => (prev + 1) % safeLogos.length)
    }, 2000) // 3s before updating

    return () => clearInterval(interval)

  }, [safeLogos.length, normalizedOffset])





  return (
    <div>
        <div>
          {/*

         
            <BlurText 
              key={logos[index]} 
              text={`${logos[index]}`}
              direction="bottom"
              stepDuration={0.2}
              />
 */}
          {currentLogo && (
          <BlurText key={`${currentLogo}-${index}`} className="items-center justify-center">
            <img
              src={currentLogo}
              alt="company-logo"
              className="h-10 w-auto"
              onError={(e) => {
                e.currentTarget.src = "/company-logos/stripe.svg";
              }}
            />
          </BlurText>
          

          
          )}

        </div>
    </div>
  )
}

export default RotatingCompanies
