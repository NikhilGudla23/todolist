# CSS Animations for TaskFlow Pro

ANIMATION_CSS = """
/* Keyframes */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes slideInLeft {
    from { transform: translateX(-20px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

@keyframes slideInBottom {
    from { transform: translateY(20px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

@keyframes popIn {
    0% { transform: scale(0.96); opacity: 0; }
    100% { transform: scale(1); opacity: 1; }
}

@keyframes rippleEffect {
    0% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.2); }
    100% { box-shadow: 0 0 0 12px rgba(99, 102, 241, 0); }
}

@keyframes shimerProgress {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}

@keyframes neonBreathing {
    0% { box-shadow: 0 0 5px rgba(239, 68, 68, 0.2), inset 0 0 2px rgba(239, 68, 68, 0.1); }
    50% { box-shadow: 0 0 15px rgba(239, 68, 68, 0.6), inset 0 0 5px rgba(239, 68, 68, 0.3); }
    100% { box-shadow: 0 0 5px rgba(239, 68, 68, 0.2), inset 0 0 2px rgba(239, 68, 68, 0.1); }
}

/* Classes */
.anim-fade-in {
    animation: fadeIn 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.anim-slide-left {
    animation: slideInLeft 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.anim-slide-bottom {
    animation: slideInBottom 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.anim-card-pop {
    animation: popIn 0.35s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

.anim-pulse-red {
    animation: neonBreathing 2s infinite ease-in-out;
}

/* Hover scales */
.hover-lift {
    transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

.hover-lift:hover {
    transform: translateY(-4px) scale(1.01) !important;
    box-shadow: 0 12px 24px -6px rgba(0, 240, 255, 0.15) !important;
}

/* Shimmer placeholder */
.shimmer {
    background: linear-gradient(90deg, #1f2937 25%, #374151 50%, #1f2937 75%);
    background-size: 200% 100%;
    animation: shimerProgress 1.5s infinite linear;
}
"""

def get_animations():
    """Return the raw CSS string for layout animations."""
    return ANIMATION_CSS
