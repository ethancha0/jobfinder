"use client";

import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { ArrowDown } from "lucide-react";
import { useState } from "react";

type FilterValues = {
  location: string;
};

type FiltersProps = {
  onLocationChange?: (location: string) => void;
  onFilterChange?: (filters: FilterValues) => void;
};

const LOCATION_OPTIONS = [
  "Remote",
  "San Francisco, CA",
  "Los Angeles, CA",
  "Seattle, WA",
  "New York City, NY",
];

const Filters = ({ onLocationChange, onFilterChange }: FiltersProps) => {
  const [selectedLocation, setSelectedLocation] = useState<string>("Location");

  const handleSelectLocation = (location: string) => {
    setSelectedLocation(location);
    onLocationChange?.(location);
    onFilterChange?.({ location });
  };

  return (
    <div className="lg:sticky lg:top-6">
      <div className="w-full rounded-2xl border border-gray-300 p-8">
        <p className="font-semibold">Filters</p>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <div className="flex items-center">
              <Button variant="outline">
                {selectedLocation}
                <ArrowDown size={15} />
              </Button>
            </div>
          </DropdownMenuTrigger>
          <DropdownMenuContent className="w-40 " align="start">
            <DropdownMenuGroup>
              {LOCATION_OPTIONS.map((location) => (
                <DropdownMenuItem
                  key={location}
                  onClick={() => handleSelectLocation(location)}
                >
                  {location}
                </DropdownMenuItem>
              ))}
            </DropdownMenuGroup>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </div>
  );
};

export default Filters;
