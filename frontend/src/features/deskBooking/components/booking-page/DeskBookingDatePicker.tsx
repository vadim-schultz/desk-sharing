import { HStack, Input, Text } from '@chakra-ui/react';

interface DeskBookingDatePickerProps {
  minDate: string;
  maxDate: string;
  value: string;
  onChange: (isoDate: string) => void;
  timezone: string;
}

export default function DeskBookingDatePicker({
  minDate,
  maxDate,
  value,
  onChange,
  timezone,
}: DeskBookingDatePickerProps) {
  return (
    <HStack gap={4} flexWrap="wrap">
      <Text fontWeight="medium">Day</Text>
      <Input
        type="date"
        min={minDate}
        max={maxDate}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        width="auto"
      />
      <Text color="fg.muted" fontSize="sm">
        Timezone: {timezone}
      </Text>
    </HStack>
  );
}
