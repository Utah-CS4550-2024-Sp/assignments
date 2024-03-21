import { useEffect, useRef } from "react";

/**
 * Container component that will scroll to the bottom
 * on mount and when the children change.
 *
 * For example, you might consider wrapping your message
 * components this scroll container.
 */
function ScrollContainer({ children }) {
  // Define references to an outer an inner div.
  const outerRef = useRef(null);
  const innerRef = useRef(null);

  // scroll function
  const scrollToBottom = (behavior) => {
    const outerHeight = outerRef.current.clientHeight;
    const innerHeight = innerRef.current.clientHeight;
    const offset = 0; // might increase based on your layout

    outerRef.current.scrollTo({
      top: innerHeight - outerHeight + offset,
      left: 0,
      behavior: behavior,
    });
  };

  // scroll to the bottom on mount
  useEffect(
    () => scrollToBottom("instant"),
    [],
  );

  // scroll to the bottom smoothly if children change
  useEffect(
    () => scrollToBottom("smooth"),
    [children],
  );

  // add to the classNames below as needed
  return (
    <div ref={outerRef} className="overflow-scroll relative">
      <div ref={innerRef} className="relative">
        {children}
      </div>
    </div>
  );
}

