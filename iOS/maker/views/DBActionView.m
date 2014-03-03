//
//  DBActionView.m
//  maker
//
//  Created by Bear on 2/23/14.
//  Copyright (c) 2014 Bear. All rights reserved.
//

#import "DBActionView.h"

@implementation DBActionView

- (id)initWithFrame:(CGRect)frame pageId:(NSString *)pid referId:(NSString *)refer action:(DBAction *)action;
{
    self = [super initWithFrame:frame];
    if (self) {
        self.pid = pid;
        self.action = action;
        self.refer = refer;
    }
    return self;
}

/*
// Only override drawRect: if you perform custom drawing.
// An empty implementation adversely affects performance during animation.
- (void)drawRect:(CGRect)rect
{
    // Drawing code
}
*/

@end
