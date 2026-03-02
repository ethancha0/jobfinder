import { Briefcase } from 'lucide-react';
import Link from 'next/link';

interface LogoProps {
  showTagline?: boolean;
  size?: 'sm' | 'md' | 'lg';
}

export function Logo({ showTagline = true, size = 'md' }: LogoProps) {
  const sizes = {
    sm: { icon: 'w-8 h-8', briefcase: 'w-4 h-4', text: 'text-lg', tagline: 'text-xs', dot: 'w-3 h-3' },
    md: { icon: 'w-10 h-10', briefcase: 'w-5 h-5', text: 'text-2xl', tagline: 'text-xs', dot: 'w-4 h-4' },
    lg: { icon: 'w-14 h-14', briefcase: 'w-7 h-7', text: 'text-3xl', tagline: 'text-sm', dot: 'w-5 h-5' },
  };

  const s = sizes[size];

  return (
    <Link href="/" className="inline-flex w-fit">
    <div className="inline-flex w-fit items-center gap-3">
      <div className="relative">
       
        <div className={`${s.icon} rounded-xl bg-gradient-to-br from-blue-950 via-blue-900 to-gray-700 flex items-center justify-center shadow-lg`}>
          <Briefcase className={`${s.briefcase} text-white`} />
        </div>
        <div className={`absolute -bottom-1 -right-1 ${s.dot} rounded-full bg-green-500 border-2 border-background`}></div>
      </div>
      <div>
        <h1 className={`${s.text} font-bold bg-gradient-to-r from-blue-950 to-blue-800 bg-clip-text text-transparent`}>
          JobFinder
        </h1>
        {showTagline && (
          <p className={`${s.tagline} text-muted-foreground`}>Instant Job Alerts</p>
        )}
        
      </div>
    
      
    </div>
    </Link>
  );
}
