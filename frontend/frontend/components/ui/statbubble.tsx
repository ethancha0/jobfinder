import { LucideIcon } from 'lucide-react'
import Image from 'next/image'
import React from 'react'
import AnimatedContent from '../AnimatedContent'

interface StatBubbleProps{
    stat: number,
    caption: string,
    Icon: LucideIcon
}


const StatBubble = ({stat, caption, Icon}: StatBubbleProps) => {
  return (
    <div className="">
        <AnimatedContent
                distance={150}
                direction="vertical"
                reverse={false}
                duration={1}
                ease="power3.out"
                initialOpacity={0}
                animateOpacity
                scale={0.2}
                threshold={0.1}
                delay={0}
                >
                <div className="flex flex-col justify-center  items-center border-2 border-gray-300 rounded-2xl p-4 w-70">
                    <div className="p-2 bg-blue-50 rounded-xl">
                    <Icon/>  
                </div>
                    


                <p className="text-3xl font-bold">{stat}+</p>
                <p className="text-md font-semibold text-gray-500">{caption}</p>


            </div>  

        </AnimatedContent>
            
    
    

    </div>
)
  
}

export default StatBubble
