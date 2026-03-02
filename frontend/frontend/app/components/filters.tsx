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

        <div className="w-full rounded-2xl border border-gray-300 p-8">
            <p className="font-semibold">Filters</p>
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <div className="flex items-center">
            <Button variant="outline">Location
                <ArrowDown size={15}/> 
            </Button>
            
        </div>
        
      </DropdownMenuTrigger>
      <DropdownMenuContent className="w-40 " align="start">
        <DropdownMenuGroup>
    
          <DropdownMenuItem>
            Remote
          </DropdownMenuItem>
          <DropdownMenuItem>
            San Francisco, CA
          </DropdownMenuItem>
          <DropdownMenuItem>
            Los Angeles, CA
          </DropdownMenuItem>
           <DropdownMenuItem>
            Seattle, WA
          </DropdownMenuItem>
           <DropdownMenuItem>
            New York City, NY
          </DropdownMenuItem>
          
        </DropdownMenuGroup>
        
    
      </DropdownMenuContent>
    </DropdownMenu>




        </div>














    </div>
  )
}

export default Filters
