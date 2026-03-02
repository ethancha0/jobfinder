import { Button } from '@/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { ArrowDown } from 'lucide-react'
import React from 'react'

const Filters = () => {
  return (
    <div className="lg:sticky lg:top-6">
        <h1 className="p-4 font-semibold">Filters</h1>

        <div className="w-full rounded-2xl border border-gray-300 p-8">
            <p className="font-semibold">Job Type</p>
            <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <div className="flex items-center">
            <Button variant="outline">All Types
                <ArrowDown size={15}/> 
            </Button>
            
        </div>
        
      </DropdownMenuTrigger>
      <DropdownMenuContent className="w-40 " align="start">
        <DropdownMenuGroup>
          <DropdownMenuLabel>Entry</DropdownMenuLabel>
          <DropdownMenuItem>
            Full-Time
           
          </DropdownMenuItem>
          <DropdownMenuItem>
            Part-Time
         
          </DropdownMenuItem>
          <DropdownMenuItem>
            Internship
          
          </DropdownMenuItem>
        </DropdownMenuGroup>
        
    
      </DropdownMenuContent>
    </DropdownMenu>



    <p className="font-semibold">Experiance Level</p>
            <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <div className="flex items-center">
            <Button variant="outline">All Types
                <ArrowDown size={15}/> 
            </Button>
            
        </div>
        
      </DropdownMenuTrigger>
      <DropdownMenuContent className="w-40" align="start">
        <DropdownMenuGroup>
          <DropdownMenuLabel>Entry</DropdownMenuLabel>
          <DropdownMenuItem>
            Full-Time
           
          </DropdownMenuItem>
          <DropdownMenuItem>
            Part-Time
         
          </DropdownMenuItem>
          <DropdownMenuItem>
            Internship
          
          </DropdownMenuItem>
        </DropdownMenuGroup>
        
    
      </DropdownMenuContent>
    </DropdownMenu>


    <p className="font-semibold">Location</p>
            <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <div className="flex items-center">
            <Button variant="outline">All Types
                <ArrowDown size={15}/> 
            </Button>
            
        </div>
        
      </DropdownMenuTrigger>
      <DropdownMenuContent className="w-40" align="start">
        <DropdownMenuGroup>
          <DropdownMenuLabel>Entry</DropdownMenuLabel>
          <DropdownMenuItem>
            Full-Time
           
          </DropdownMenuItem>
          <DropdownMenuItem>
            Part-Time
         
          </DropdownMenuItem>
          <DropdownMenuItem>
            Internship
          
          </DropdownMenuItem>
        </DropdownMenuGroup>
        
    
      </DropdownMenuContent>
    </DropdownMenu>



        </div>














    </div>
  )
}

export default Filters
