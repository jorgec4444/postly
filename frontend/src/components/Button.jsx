// Copyright © 2026 Jorge Vinagre
// SPDX-License-Identifier: AGPL-3.0-only WITH Commons-Clause

/**
 * Reusable Button component.
 *
 * Variants:
 *   primary   — green gradient, white text (default)
 *   secondary — white bg, gray border
 *   danger    — red border, red text
 *   ghost     — no border, subtle hover
 *
 * Sizes:
 *   sm  — text-xs, px-3 py-1.5
 *   md  — text-sm, px-4 py-2.5 (default)
 *   lg  — text-sm, px-5 py-3
 */

import { Loader2 } from "lucide-react";

const VARIANTS = {
  primary:
    "bg-gradient-to-br from-primary to-accent text-white hover:opacity-90 shadow-sm disabled:opacity-40",
  secondary:
    "bg-white border border-gray-200 text-gray-700 hover:border-primary hover:text-primary disabled:opacity-40",
  danger:
    "bg-white border border-red-200 text-red-500 hover:bg-red-50 disabled:opacity-40",
  ghost:
    "text-gray-500 hover:text-gray-700 hover:bg-gray-100 disabled:opacity-40",
};

const SIZES = {
  sm: "text-xs px-3 py-1.5 rounded-xl",
  md: "text-sm px-4 py-2.5 rounded-xl",
  lg: "text-sm px-5 py-3 rounded-xl",
};

export default function Button({
  children,
  variant = "primary",
  size = "md",
  loading = false,
  disabled = false,
  onClick,
  className = "",
  type = "button",
  ...props
}) {
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled || loading}
      className={`
        inline-flex items-center justify-center gap-2
        font-semibold transition-all
        disabled:cursor-not-allowed
        ${VARIANTS[variant]}
        ${SIZES[size]}
        ${className}
      `}
      {...props}
    >
      {loading && (
        <Loader2 className="w-3.5 h-3.5 animate-spin flex-shrink-0" />
      )}
      {children}
    </button>
  );
}
