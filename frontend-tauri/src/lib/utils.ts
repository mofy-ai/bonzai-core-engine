// 💜 MAMA BEAR'S UTILITY FUNCTIONS - SPREADING LOVE EVERYWHERE! ✨
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

// 🎨 Beautiful class name merging with love
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// 💜 Mama Bear's encouraging console logs
export function logWithLove(message: string, type: 'info' | 'success' | 'warning' | 'error' = 'info') {
  const emoji = {
    info: '💜',
    success: '🎉',
    warning: '⚠️',
    error: '🚨'
  }[type];
  
  console.log(`${emoji} Mama Bear: ${message}`);
}

// 🚀 Format file sizes with love
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// 💜 Debounce function for smooth interactions
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout;
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}
